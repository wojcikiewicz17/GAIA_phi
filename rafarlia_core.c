// rafaelia_core.c
#include <errno.h>
#include <openssl/evp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>

#define MAX_PATH 4096
#define MAX_EXTS 64

typedef struct {
    const char *base_path;
    const char *json_path;
    const char *md_path;
    int include_hidden;
    int follow_symlinks;
    int hash_enabled;
    int max_depth;
    long max_size;
    const char *exts[MAX_EXTS];
    size_t ext_count;
} Config;

typedef struct {
    long files_indexed;
    long files_hashed;
    long files_skipped;
    long errors;
    long long total_bytes;
} Stats;

static const char *default_exts[] = {
    ".c", ".h", ".py", ".md", ".json", ".txt", ".sh"
};

static int ends_with(const char *name, const char *suffix) {
    size_t n = strlen(name), s = strlen(suffix);
    return n >= s && strcmp(name + n - s, suffix) == 0;
}

static int has_valid_ext(const char *name, const Config *cfg) {
    for (size_t i = 0; i < cfg->ext_count; i++)
        if (ends_with(name, cfg->exts[i])) return 1;
    return 0;
}

static void sha3_file(const char *path, char *out, size_t outlen) {
    unsigned char hash[32], buf[4096];
    EVP_MD_CTX *ctx = EVP_MD_CTX_new();
    FILE *f = fopen(path, "rb");
    if (!ctx || !f) { snprintf(out, outlen, "ERROR"); return; }

    EVP_DigestInit_ex(ctx, EVP_sha3_256(), NULL);
    size_t n;
    while ((n = fread(buf, 1, sizeof(buf), f)) > 0)
        EVP_DigestUpdate(ctx, buf, n);
    EVP_DigestFinal_ex(ctx, hash, NULL);
    EVP_MD_CTX_free(ctx);
    fclose(f);

    for (int i = 0; i < 32; i++)
        snprintf(out + i*2, outlen - i*2, "%02x", hash[i]);
}

static void scan(const char *base, const Config *cfg, FILE *json, FILE *md,
                 int *first, Stats *stats, int depth) {
    DIR *dir = opendir(base);
    if (!dir) { stats->errors++; return; }

    struct dirent *ent;
    while ((ent = readdir(dir))) {
        if (!strcmp(ent->d_name, ".") || !strcmp(ent->d_name, "..")) continue;
        if (!cfg->include_hidden && ent->d_name[0] == '.') continue;

        char path[MAX_PATH];
        snprintf(path, sizeof(path), "%s/%s", base, ent->d_name);

        struct stat st;
        if (lstat(path, &st) != 0) { stats->errors++; continue; }

        if (S_ISDIR(st.st_mode)) {
            if (cfg->max_depth >= 0 && depth >= cfg->max_depth) continue;
            scan(path, cfg, json, md, first, stats, depth + 1);
        } else if (S_ISREG(st.st_mode) && has_valid_ext(ent->d_name, cfg)) {
            if (cfg->max_size >= 0 && st.st_size > cfg->max_size) continue;

            char hash[65] = "DISABLED";
            if (cfg->hash_enabled) {
                sha3_file(path, hash, sizeof(hash));
                stats->files_hashed++;
            }

            if (!*first) fprintf(json, ",\n");
            *first = 0;
            fprintf(json, "  {\"path\":\"%s\",\"size\":%ld,\"sha3\":\"%s\"}", path, st.st_size, hash);
            fprintf(md, "- `%s` (%ld bytes) sha3=%.*s…\n", path, st.st_size, 16, hash);

            stats->files_indexed++;
            stats->total_bytes += st.st_size;
        }
    }
    closedir(dir);
}

int main(void) {
    Config cfg = {
        .base_path = ".",
        .json_path = "RAFAELIA_CYCLE_INDEX.json",
        .md_path = "RAFAELIA_CYCLE_REPORT.md",
        .hash_enabled = 1,
        .max_depth = -1,
        .max_size = -1
    };

    cfg.ext_count = sizeof(default_exts)/sizeof(default_exts[0]);
    for (size_t i = 0; i < cfg.ext_count; i++)
        cfg.exts[i] = default_exts[i];

    FILE *json = fopen(cfg.json_path, "w");
    FILE *md = fopen(cfg.md_path, "w");
    if (!json || !md) { perror("open"); return 1; }

    Stats stats = {0};
    int first = 1;

    fprintf(json, "[\n");
    fprintf(md, "# RAFAELIA REPORT\n\n## Files\n\n");

    scan(cfg.base_path, &cfg, json, md, &first, &stats, 0);

    fprintf(json, "\n]\n");
    fprintf(md, "\n## Summary\n- Files: %ld\n- Bytes: %lld\n- Errors: %ld\n",
            stats.files_indexed, stats.total_bytes, stats.errors);

    fclose(json); fclose(md);
    printf("[OK] Generated reports.\n");
    return 0;
}
