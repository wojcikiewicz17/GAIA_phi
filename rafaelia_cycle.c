/*
  RAFAELIA_CYCLE — deterministic index + SHA3-256 + JSON/JSONL/MD/CSV report
  Focus: auditability, reproducibility, Termux-friendly.

  Build (Termux):
    pkg install clang openssl -y
    clang -O2 -Wall -Wextra rafaelia_cycle.c -o rafaelia_cycle -lssl -lcrypto

  Build (Linux):
    sudo apt-get install -y gcc libssl-dev
    gcc -O2 -Wall -Wextra rafaelia_cycle.c -o rafaelia_cycle -lssl -lcrypto

  Run:
    ./rafaelia_cycle --base . --out-dir out
*/

#define _XOPEN_SOURCE 700
#include <errno.h>
#include <limits.h>
#include <openssl/evp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <time.h>

#define RC_MAX_PATH 4096
#define RC_HASH_BYTES 32
#define RC_HASH_HEX  (RC_HASH_BYTES * 2)

typedef struct {
  const char *base;
  const char *out_dir;
  const char *json_name;
  const char *jsonl_name;
  const char *md_name;
  const char *csv_name;

  int include_hidden;
  int follow_symlinks;
  int enable_hash;
  int emit_arch;
  int emit_opps;
  int emit_json;
  int emit_jsonl;
  int emit_md;
  int emit_csv;
  int dry_run;
  int strict;

  int max_depth;        /* -1 = unlimited */
  long max_size;        /* -1 = unlimited */

  const char **exts;    /* array of ".c", ".py"... */
  size_t ext_count;
} RC_Config;

typedef struct {
  long files_indexed;
  long files_hashed;
  long files_skipped;
  long errors;
  long long total_bytes;
} RC_Stats;

/* --------- small helpers --------- */
static int rc_is_hidden(const char *name) { return name && name[0] == '.'; }

static int rc_ends_with(const char *s, const char *suffix) {
  size_t ls = strlen(s), lf = strlen(suffix);
  if (lf > ls) return 0;
  return strcmp(s + (ls - lf), suffix) == 0;
}

static int rc_has_valid_ext(const RC_Config *cfg, const char *name) {
  if (!cfg->exts || cfg->ext_count == 0) return 1; /* no filter = accept all */
  for (size_t i = 0; i < cfg->ext_count; i++) {
    if (rc_ends_with(name, cfg->exts[i])) return 1;
  }
  return 0;
}

static void rc_json_escape(FILE *out, const char *value) {
  for (const unsigned char *p = (const unsigned char *)value; *p; p++) {
    switch (*p) {
      case '\"': fputs("\\\"", out); break;
      case '\\': fputs("\\\\", out); break;
      case '\b': fputs("\\b", out); break;
      case '\f': fputs("\\f", out); break;
      case '\n': fputs("\\n", out); break;
      case '\r': fputs("\\r", out); break;
      case '\t': fputs("\\t", out); break;
      default:
        if (*p < 0x20) fprintf(out, "\\u%04x", *p);
        else fputc(*p, out);
    }
  }
}

static int rc_mkdir_p(const char *path) {
  char tmp[RC_MAX_PATH];
  size_t len = strlen(path);
  if (len == 0 || len >= sizeof(tmp)) return -1;
  strcpy(tmp, path);

  if (tmp[len - 1] == '/') tmp[len - 1] = 0;

  for (char *p = tmp + 1; *p; p++) {
    if (*p == '/') {
      *p = 0;
      if (mkdir(tmp, 0755) != 0 && errno != EEXIST) return -1;
      *p = '/';
    }
  }
  if (mkdir(tmp, 0755) != 0 && errno != EEXIST) return -1;
  return 0;
}

static void rc_now_local(char out[64]) {
  time_t now = time(NULL);
  struct tm tmv;
  memset(&tmv, 0, sizeof(tmv));
  localtime_r(&now, &tmv);
  strftime(out, 64, "%Y-%m-%d %H:%M:%S", &tmv);
}

static double rc_now_seconds(void) {
  struct timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

/* --------- SHA3-256 (OpenSSL EVP) --------- */
static int rc_sha3_256_file(const char *path, char hex_out[RC_HASH_HEX + 1]) {
  unsigned char hash[RC_HASH_BYTES];
  unsigned char buf[8192];

  FILE *f = fopen(path, "rb");
  if (!f) return -1;

  EVP_MD_CTX *ctx = EVP_MD_CTX_new();
  if (!ctx) { fclose(f); return -1; }

  if (EVP_DigestInit_ex(ctx, EVP_sha3_256(), NULL) != 1) {
    EVP_MD_CTX_free(ctx); fclose(f); return -1;
  }

  size_t n = 0;
  while ((n = fread(buf, 1, sizeof(buf), f)) > 0) {
    if (EVP_DigestUpdate(ctx, buf, n) != 1) {
      EVP_MD_CTX_free(ctx); fclose(f); return -1;
    }
  }
  if (ferror(f)) { EVP_MD_CTX_free(ctx); fclose(f); return -1; }

  if (EVP_DigestFinal_ex(ctx, hash, NULL) != 1) {
    EVP_MD_CTX_free(ctx); fclose(f); return -1;
  }

  EVP_MD_CTX_free(ctx);
  fclose(f);

  for (int i = 0; i < RC_HASH_BYTES; i++) sprintf(hex_out + (i * 2), "%02x", hash[i]);
  hex_out[RC_HASH_HEX] = 0;
  return 0;
}

/* --------- architecture/opportunities (lightweight) --------- */
static const char *kLayers[7] = {
  "Camada 1: Percepcao & Coleta",
  "Camada 2: Ingestao & Validacao",
  "Camada 3: Normalizacao & Vetorizacao",
  "Camada 4: Indexacao & Persistencia",
  "Camada 5: Raciocinio & Planejamento",
  "Camada 6: Sintese & Comunicacao",
  "Camada 7: Governanca & Etica"
};

static const char *kOpps[42] = {
  "Escopo dinamico (profundidade, filtros)",
  "Filtro inteligente por extensao e tamanho",
  "Determinismo garantido por ordenacao",
  "Symlink safety (modo seguro por padrao)",
  "Snapshot verificavel por SHA3-256",
  "Diff entre snapshots (baseline vs delta)",
  "Deduplicacao por hash",
  "Indice SQLite para busca rapida",
  "Exportacao CSV/TSV",
  "Log de performance (bytes/s, files/s)",
  "Ranking de risco (binarios, gigantes, suspeitos)",
  "Whitelist/blacklist por diretorio",
  "Cache incremental por mtime+size",
  "Batching de IO para performance",
  "Modo dry-run e modo strict",
  "Relatorio para stakeholders",
  "Trilha de auditoria imutavel",
  "Compatibilidade Termux offline",
  "Normalizacao soberana de paths",
  "Manifesto de release",
  "Quarentena de artefatos binarios",
  "Tagging semantico (futuro RAG)",
  "Export para base vetorial",
  "Observabilidade (erros por tipo)",
  "Assinatura/selagem (futuro)",
  "Politicas de exclusao seguras",
  "Matriz SSM (camadas x modulos)",
  "Controle de memoria",
  "Modo verboso/silencioso",
  "Controle de quota por tamanho",
  "Detectar arquivos vazios",
  "Detectar arvore mais densa",
  "Mapa de calor por caminho",
  "Pipeline CI",
  "Compatibilidade com zips (futuro)",
  "Multi-hash (BLAKE3 opcional)",
  "Parallel digest (futuro)",
  "Indice federado multi-repo",
  "Registry de datasets",
  "Remediacao sugerida",
  "Governanca Ethica",
  "Portal FIAT (alinhamento)"
};

/* --------- deterministic directory scan --------- */

typedef struct {
  FILE *json;
  FILE *jsonl;
  FILE *md;
  FILE *csv;
  int first_json;
  RC_Config cfg;
  RC_Stats st;
  char base_abs[RC_MAX_PATH];
  size_t base_abs_len;
} RC_Ctx;

static int rc_cmp_str(const void *a, const void *b) {
  const char *sa = *(const char **)a;
  const char *sb = *(const char **)b;
  return strcmp(sa, sb);
}

static int rc_relpath(RC_Ctx *ctx, const char *abs_path, char out[RC_MAX_PATH]) {
  size_t n = ctx->base_abs_len;
  if (strncmp(abs_path, ctx->base_abs, n) != 0) return -1;
  const char *p = abs_path + n;
  if (*p == '/') p++;
  snprintf(out, RC_MAX_PATH, "%s", p);
  return 0;
}

static void rc_emit_file(RC_Ctx *ctx, const char *rel, long long size, const char *hash_or_tag) {
  if (ctx->cfg.emit_json) {
    if (!ctx->first_json) fputs(",\n", ctx->json);
    ctx->first_json = 0;

    fputs("    {\"path\":\"", ctx->json);
    rc_json_escape(ctx->json, rel);
    fprintf(ctx->json, "\",\"size\":%lld,\"sha3_256\":\"%s\"}", size, hash_or_tag);
  }

  if (ctx->cfg.emit_jsonl) {
    fputs("{\"path\":\"", ctx->jsonl);
    rc_json_escape(ctx->jsonl, rel);
    fprintf(ctx->jsonl, "\",\"size\":%lld,\"sha3_256\":\"%s\"}\n", size, hash_or_tag);
  }

  if (ctx->cfg.emit_md) {
    fprintf(ctx->md, "- `%s` (%lld bytes) sha3=%.*s...\n", rel, size, 16, hash_or_tag);
  }

  if (ctx->cfg.emit_csv) {
    fprintf(ctx->csv, "\"%s\",%lld,\"%s\"\n", rel, size, hash_or_tag);
  }
}

static void rc_scan(RC_Ctx *ctx, const char *dir_abs, int depth) {
  if (ctx->cfg.max_depth >= 0 && depth > ctx->cfg.max_depth) {
    ctx->st.files_skipped++;
    return;
  }

  DIR *d = opendir(dir_abs);
  if (!d) {
    ctx->st.errors++;
    if (ctx->cfg.strict) fprintf(stderr, "[ERRO] opendir: %s (errno=%d)\n", dir_abs, errno);
    return;
  }

  /* collect names then sort => determinism */
  size_t cap = 128, cnt = 0;
  char **names = (char **)calloc(cap, sizeof(char *));
  if (!names) {
    closedir(d);
    ctx->st.errors++;
    if (ctx->cfg.strict) fprintf(stderr, "[ERRO] memoria insuficiente\n");
    return;
  }

  struct dirent *ent;
  while ((ent = readdir(d)) != NULL) {
    if (!strcmp(ent->d_name, ".") || !strcmp(ent->d_name, "..")) continue;
    if (!ctx->cfg.include_hidden && rc_is_hidden(ent->d_name)) continue;

    if (cnt == cap) {
      cap *= 2;
      char **tmp = (char **)realloc(names, cap * sizeof(char *));
      if (!tmp) break;
      names = tmp;
    }
    names[cnt++] = strdup(ent->d_name);
  }
  closedir(d);

  qsort(names, cnt, sizeof(char *), rc_cmp_str);

  for (size_t i = 0; i < cnt; i++) {
    if (!names[i]) continue;

    char path_abs[RC_MAX_PATH];
    snprintf(path_abs, sizeof(path_abs), "%s/%s", dir_abs, names[i]);

    struct stat st;
    int ok = ctx->cfg.follow_symlinks ? stat(path_abs, &st) : lstat(path_abs, &st);
    if (ok != 0) {
      ctx->st.errors++;
      if (ctx->cfg.strict) fprintf(stderr, "[ERRO] stat: %s (errno=%d)\n", path_abs, errno);
      free(names[i]);
      continue;
    }

    if (S_ISLNK(st.st_mode) && !ctx->cfg.follow_symlinks) {
      ctx->st.files_skipped++;
      free(names[i]);
      continue;
    }

    if (S_ISDIR(st.st_mode)) {
      rc_scan(ctx, path_abs, depth + 1);
      free(names[i]);
      continue;
    }

    if (!S_ISREG(st.st_mode)) {
      ctx->st.files_skipped++;
      free(names[i]);
      continue;
    }

    if (ctx->cfg.max_size >= 0 && st.st_size > ctx->cfg.max_size) {
      ctx->st.files_skipped++;
      free(names[i]);
      continue;
    }

    if (!rc_has_valid_ext(&ctx->cfg, names[i])) {
      ctx->st.files_skipped++;
      free(names[i]);
      continue;
    }

    char rel[RC_MAX_PATH];
    if (rc_relpath(ctx, path_abs, rel) != 0) {
      ctx->st.errors++;
      if (ctx->cfg.strict) fprintf(stderr, "[ERRO] relpath: %s\n", path_abs);
      free(names[i]);
      continue;
    }

    char hash[RC_HASH_HEX + 1];
    if (ctx->cfg.enable_hash) {
      if (rc_sha3_256_file(path_abs, hash) != 0) {
        strcpy(hash, "ERROR");
        ctx->st.errors++;
        if (ctx->cfg.strict) fprintf(stderr, "[ERRO] hash: %s\n", path_abs);
      } else {
        ctx->st.files_hashed++;
      }
    } else {
      strcpy(hash, "DISABLED");
    }

    rc_emit_file(ctx, rel, (long long)st.st_size, hash);
    ctx->st.files_indexed++;
    ctx->st.total_bytes += (long long)st.st_size;

    free(names[i]);
  }

  free(names);
}

static void rc_usage(const char *prog) {
  printf("Uso: %s [opcoes]\n", prog);
  printf("  --base <path>            Diretorio base (padrao: .)\n");
  printf("  --out-dir <path>         Diretorio de saida (padrao: out)\n");
  printf("  --json <name>            Nome do arquivo JSON (padrao: RAFAELIA_CYCLE_INDEX.json)\n");
  printf("  --jsonl <name>           Nome do arquivo JSONL (padrao: RAFAELIA_CYCLE_INDEX.jsonl)\n");
  printf("  --md <name>              Nome do arquivo MD (padrao: RAFAELIA_CYCLE_REPORT.md)\n");
  printf("  --csv <name>             Nome do arquivo CSV (padrao: RAFAELIA_CYCLE_REPORT.csv)\n");
  printf("  --ext <.c,.h,.py>        Filtra extensoes (padrao: tudo)\n");
  printf("  --include-hidden         Inclui ocultos\n");
  printf("  --follow-symlinks        Segue symlinks (nao recomendado)\n");
  printf("  --max-depth <n>          Profundidade maxima (padrao: ilimitado)\n");
  printf("  --max-size <bytes>       Tamanho maximo de arquivo (padrao: ilimitado)\n");
  printf("  --no-hash                Desativa SHA3\n");
  printf("  --no-arch                Remove matriz arquitetural\n");
  printf("  --no-opps                Remove oportunidades\n");
  printf("  --no-json                Desativa JSON\n");
  printf("  --no-jsonl               Desativa JSONL\n");
  printf("  --no-md                  Desativa Markdown\n");
  printf("  --no-csv                 Desativa CSV\n");
  printf("  --dry-run                Varre sem gravar arquivos\n");
  printf("  --strict                 Falha em erros (retorno != 0)\n");
  printf("  --help                   Ajuda\n");
}

static void rc_parse_exts(RC_Config *cfg, const char *csv) {
  if (!csv || !*csv) return;
  /* count */
  size_t count = 1;
  for (const char *p = csv; *p; p++) if (*p == ',') count++;
  const char **arr = (const char **)calloc(count, sizeof(char *));
  if (!arr) return;

  char *dup = strdup(csv);
  if (!dup) { free(arr); return; }

  size_t idx = 0;
  char *tok = strtok(dup, ",");
  while (tok && idx < count) {
    while (*tok == ' ') tok++;
    size_t len = strlen(tok);
    while (len > 0 && tok[len - 1] == ' ') { tok[len - 1] = 0; len--; }
    if (len > 0) {
      if (tok[0] != '.') {
        /* prepend '.' */
        char *withdot = (char *)malloc(len + 2);
        if (withdot) { withdot[0] = '.'; memcpy(withdot + 1, tok, len + 1); arr[idx++] = withdot; }
      } else {
        arr[idx++] = strdup(tok);
      }
    }
    tok = strtok(NULL, ",");
  }
  free(dup);

  cfg->exts = arr;
  cfg->ext_count = idx;
}

int main(int argc, char **argv) {
  RC_Config cfg;
  memset(&cfg, 0, sizeof(cfg));

  cfg.base = ".";
  cfg.out_dir = "out";
  cfg.json_name = "RAFAELIA_CYCLE_INDEX.json";
  cfg.jsonl_name = "RAFAELIA_CYCLE_INDEX.jsonl";
  cfg.md_name = "RAFAELIA_CYCLE_REPORT.md";
  cfg.csv_name = "RAFAELIA_CYCLE_REPORT.csv";
  cfg.include_hidden = 0;
  cfg.follow_symlinks = 0;
  cfg.enable_hash = 1;
  cfg.emit_arch = 1;
  cfg.emit_opps = 1;
  cfg.emit_json = 1;
  cfg.emit_jsonl = 1;
  cfg.emit_md = 1;
  cfg.emit_csv = 0;
  cfg.dry_run = 0;
  cfg.strict = 0;
  cfg.max_depth = -1;
  cfg.max_size = -1;

  const char *ext_csv = NULL;

  for (int i = 1; i < argc; i++) {
    if (!strcmp(argv[i], "--base") && i + 1 < argc) cfg.base = argv[++i];
    else if (!strcmp(argv[i], "--out-dir") && i + 1 < argc) cfg.out_dir = argv[++i];
    else if (!strcmp(argv[i], "--json") && i + 1 < argc) cfg.json_name = argv[++i];
    else if (!strcmp(argv[i], "--jsonl") && i + 1 < argc) cfg.jsonl_name = argv[++i];
    else if (!strcmp(argv[i], "--md") && i + 1 < argc) cfg.md_name = argv[++i];
    else if (!strcmp(argv[i], "--csv") && i + 1 < argc) cfg.csv_name = argv[++i];
    else if (!strcmp(argv[i], "--ext") && i + 1 < argc) ext_csv = argv[++i];
    else if (!strcmp(argv[i], "--include-hidden")) cfg.include_hidden = 1;
    else if (!strcmp(argv[i], "--follow-symlinks")) cfg.follow_symlinks = 1;
    else if (!strcmp(argv[i], "--max-depth") && i + 1 < argc) cfg.max_depth = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--max-size") && i + 1 < argc) cfg.max_size = atol(argv[++i]);
    else if (!strcmp(argv[i], "--no-hash")) cfg.enable_hash = 0;
    else if (!strcmp(argv[i], "--no-arch")) cfg.emit_arch = 0;
    else if (!strcmp(argv[i], "--no-opps")) cfg.emit_opps = 0;
    else if (!strcmp(argv[i], "--no-json")) cfg.emit_json = 0;
    else if (!strcmp(argv[i], "--no-jsonl")) cfg.emit_jsonl = 0;
    else if (!strcmp(argv[i], "--no-md")) cfg.emit_md = 0;
    else if (!strcmp(argv[i], "--no-csv")) cfg.emit_csv = 0;
    else if (!strcmp(argv[i], "--dry-run")) cfg.dry_run = 1;
    else if (!strcmp(argv[i], "--strict")) cfg.strict = 1;
    else if (!strcmp(argv[i], "--help")) { rc_usage(argv[0]); return 0; }
    else { fprintf(stderr, "Opcao invalida: %s\n", argv[i]); rc_usage(argv[0]); return 2; }
  }

  if (!cfg.emit_json && !cfg.emit_jsonl && !cfg.emit_md && !cfg.emit_csv) {
    fprintf(stderr, "[ERRO] Nenhum formato selecionado.\n");
    return 2;
  }

  if (ext_csv) rc_parse_exts(&cfg, ext_csv);

  char base_abs[RC_MAX_PATH];
  if (!realpath(cfg.base, base_abs)) {
    fprintf(stderr, "[ERRO] base invalida: %s (errno=%d)\n", cfg.base, errno);
    return 2;
  }

  if (!cfg.dry_run && rc_mkdir_p(cfg.out_dir) != 0) {
    fprintf(stderr, "[ERRO] nao consegui criar out-dir: %s (errno=%d)\n", cfg.out_dir, errno);
    return 2;
  }

  char json_path[RC_MAX_PATH], jsonl_path[RC_MAX_PATH], md_path[RC_MAX_PATH], csv_path[RC_MAX_PATH];
  snprintf(json_path, sizeof(json_path), "%s/%s", cfg.out_dir, cfg.json_name);
  snprintf(jsonl_path, sizeof(jsonl_path), "%s/%s", cfg.out_dir, cfg.jsonl_name);
  snprintf(md_path, sizeof(md_path), "%s/%s", cfg.out_dir, cfg.md_name);
  snprintf(csv_path, sizeof(csv_path), "%s/%s", cfg.out_dir, cfg.csv_name);

  FILE *json = NULL;
  FILE *jsonl = NULL;
  FILE *md = NULL;
  FILE *csv = NULL;
  if (!cfg.dry_run) {
    if (cfg.emit_json) json = fopen(json_path, "w");
    if (cfg.emit_jsonl) jsonl = fopen(jsonl_path, "w");
    if (cfg.emit_md) md = fopen(md_path, "w");
    if (cfg.emit_csv) csv = fopen(csv_path, "w");
    if ((cfg.emit_json && !json) || (cfg.emit_jsonl && !jsonl) || (cfg.emit_md && !md) || (cfg.emit_csv && !csv)) {
      fprintf(stderr, "[ERRO] abrir saidas falhou (errno=%d)\n", errno);
      if (json) fclose(json);
      if (jsonl) fclose(jsonl);
      if (md) fclose(md);
      if (csv) fclose(csv);
      return 2;
    }
  }

  RC_Ctx ctx;
  memset(&ctx, 0, sizeof(ctx));
  ctx.json = json;
  ctx.jsonl = jsonl;
  ctx.md = md;
  ctx.csv = csv;
  ctx.first_json = 1;
  ctx.cfg = cfg;
  strncpy(ctx.base_abs, base_abs, sizeof(ctx.base_abs) - 1);
  ctx.base_abs_len = strlen(ctx.base_abs);

  char tbuf[64];
  rc_now_local(tbuf);

  double t0 = rc_now_seconds();

  if (!cfg.dry_run && cfg.emit_json) {
    /* JSON header */
    fputs("{\n  \"meta\": {\n", ctx.json);
    fputs("    \"generated_at\": \"", ctx.json); rc_json_escape(ctx.json, tbuf); fputs("\",\n", ctx.json);
    fputs("    \"base\": \"", ctx.json); rc_json_escape(ctx.json, ctx.base_abs); fputs("\",\n", ctx.json);
    fprintf(ctx.json, "    \"include_hidden\": %s,\n", cfg.include_hidden ? "true" : "false");
    fprintf(ctx.json, "    \"follow_symlinks\": %s,\n", cfg.follow_symlinks ? "true" : "false");
    fprintf(ctx.json, "    \"hash\": %s,\n", cfg.enable_hash ? "true" : "false");
    fprintf(ctx.json, "    \"max_depth\": %d,\n", cfg.max_depth);
    fprintf(ctx.json, "    \"max_size\": %ld,\n", cfg.max_size);

    fputs("    \"extensions\": [", ctx.json);
    for (size_t i = 0; i < cfg.ext_count; i++) {
      if (i) fputs(",", ctx.json);
      fputs("\"", ctx.json); rc_json_escape(ctx.json, cfg.exts[i]); fputs("\"", ctx.json);
    }
    fputs("]\n  },\n", ctx.json);

    fputs("  \"files\": [\n", ctx.json);
  }

  if (!cfg.dry_run && cfg.emit_md) {
    /* Markdown header */
    fprintf(ctx.md, "# RAFAELIA — Cycle Report\n\n");
    fprintf(ctx.md, "**Generated at:** %s\n\n", tbuf);
    fprintf(ctx.md, "**Base:** `%s`\n\n", ctx.base_abs);
    fprintf(ctx.md, "## Files indexed\n\n");
  }

  if (!cfg.dry_run && cfg.emit_csv) {
    fprintf(ctx.csv, "path,size,sha3_256\n");
  }

  rc_scan(&ctx, ctx.base_abs, 0);

  double t1 = rc_now_seconds();
  double elapsed = t1 - t0;
  double bytes_per_s = (elapsed > 0.0) ? ((double)ctx.st.total_bytes / elapsed) : 0.0;

  if (!cfg.dry_run && cfg.emit_json) {
    /* footer JSON */
    fputs("\n  ],\n  \"summary\": {\n", ctx.json);
    fprintf(ctx.json, "    \"files_indexed\": %ld,\n", ctx.st.files_indexed);
    fprintf(ctx.json, "    \"files_hashed\": %ld,\n", ctx.st.files_hashed);
    fprintf(ctx.json, "    \"files_skipped\": %ld,\n", ctx.st.files_skipped);
    fprintf(ctx.json, "    \"errors\": %ld,\n", ctx.st.errors);
    fprintf(ctx.json, "    \"total_bytes\": %lld,\n", ctx.st.total_bytes);
    fprintf(ctx.json, "    \"elapsed_seconds\": %.6f,\n", elapsed);
    fprintf(ctx.json, "    \"bytes_per_s\": %.3f\n", bytes_per_s);
    fputs("  }\n}\n", ctx.json);
  }

  if (!cfg.dry_run && cfg.emit_md) {
    /* footer MD */
    fprintf(ctx.md, "\n## Summary\n\n");
    fprintf(ctx.md, "- Files indexed: %ld\n", ctx.st.files_indexed);
    fprintf(ctx.md, "- Files hashed: %ld\n", ctx.st.files_hashed);
    fprintf(ctx.md, "- Files skipped: %ld\n", ctx.st.files_skipped);
    fprintf(ctx.md, "- Errors: %ld\n", ctx.st.errors);
    fprintf(ctx.md, "- Total bytes: %lld\n", ctx.st.total_bytes);
    fprintf(ctx.md, "- Elapsed seconds: %.6f\n", elapsed);
    fprintf(ctx.md, "- Bytes per second: %.3f\n", bytes_per_s);
    fprintf(ctx.md, "- SHA3 enabled: %s\n", cfg.enable_hash ? "yes" : "no");

    if (cfg.emit_opps) {
      fprintf(ctx.md, "\n## 42 Opportunities\n\n");
      for (size_t i = 0; i < 42; i++) fprintf(ctx.md, "%2zu. %s\n", i + 1, kOpps[i]);
    }

    if (cfg.emit_arch) {
      fprintf(ctx.md, "\n## Architecture (7 layers)\n\n");
      for (size_t i = 0; i < 7; i++) fprintf(ctx.md, "- %s\n", kLayers[i]);
    }
  }

  if (json) fclose(json);
  if (jsonl) fclose(jsonl);
  if (md) fclose(md);
  if (csv) fclose(csv);

  if (cfg.dry_run) {
    printf("[DRY-RUN] files=%ld bytes=%lld errors=%ld elapsed=%.6f\n",
           ctx.st.files_indexed, ctx.st.total_bytes, ctx.st.errors, elapsed);
  } else {
    printf("[OK] Generated:\n");
    if (cfg.emit_json) printf("- %s\n", json_path);
    if (cfg.emit_jsonl) printf("- %s\n", jsonl_path);
    if (cfg.emit_md) printf("- %s\n", md_path);
    if (cfg.emit_csv) printf("- %s\n", csv_path);
  }

  if (ctx.st.errors > 0) return cfg.strict ? 2 : 1;
  return 0;
}
