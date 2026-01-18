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
    const char *name;
    const char *role;
} Module;

typedef struct {
    const char *layer_name;
    const Module *modules;
    size_t module_count;
} Layer;

typedef struct {
    const char *name;
    const char *purpose;
} PipelineStage;

typedef struct {
    const char *stage;
    const char *owner;
    const char *responsibility;
    const char *output;
} StageResponsibility;

typedef struct {
    const char *base_path;
    const char *json_path;
    const char *md_path;
    int include_hidden;
    int follow_symlinks;
    int hash_enabled;
    int emit_architecture;
    int emit_opportunities;
    int max_depth;
    long max_size;
    const char *exts[MAX_EXTS];
    size_t ext_count;
    int owns_exts;
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

static const char *opportunities[42] = {
    "Extensao dinamica de formatos e filtros por dominio",
    "Deteccao de duplicidade por hash e tamanho",
    "Exportacao CSV para integração legada",
    "Filtro por janela temporal (mtime/ctime)",
    "Relatorio com densidade de extensoes",
    "Indexacao incremental com cache local",
    "Suporte a lista de exclusao por padrao",
    "Compatibilidade com modo somente leitura",
    "Sinalizacao de arquivos vazios",
    "Ranking por tamanho e criticidade",
    "Captura de metadados de permissao",
    "Deteccao de links simbolicos",
    "Modo de auditoria criptografica",
    "Compatibilidade com ambientes offline",
    "Monitoramento por intervalo de tempo",
    "Geracao de manifesto de release",
    "Deteccao de arquivos temporarios",
    "Segmentacao por camada arquitetural",
    "Roteiro de performance por IO",
    "Exportacao para base vetorial",
    "Relatorio de risco e conformidade",
    "Metadados de proprietario/UID",
    "Somatorio de bytes por extensao",
    "Integracao com pipelines CI",
    "Indice para busca semantica",
    "Marcacao de arquivos de treinamento",
    "Compatibilidade com armazenamento SSM",
    "Geração de checksum alternativo",
    "Resumo heuristico por diretorio",
    "Filtros por profundidade maxima",
    "Deteccao de arvore mais densa",
    "Sinalizacao de arquivos com erro",
    "Anotacao de prioridades",
    "Mapa de calor por caminho",
    "Modo silencioso e verboso",
    "Compatibilidade com ANSI color",
    "Catalogo de camadas e modulos",
    "Pipeline para limpeza de lixo",
    "Modo sandbox para analise",
    "Relatorio para stakeholders",
    "Metricas de cobertura",
    "Snapshot comparativo"
};

static const Module layer1_modules[] = {
    {"RAFAELIA_CORE", "Identidade e contexto raiz"},
    {"ARKREΩ_CORE", "Orquestracao de base"},
    {"STACK128K_HYPER", "Buffer de operacao"},
    {"ALG_RAFAELIA_RING", "Ciclos de fluxo"},
    {"AETHER", "Hash e integridade"}
};

static const Module layer2_modules[] = {
    {"RAF_VECTOR", "Indexacao vetorial"},
    {"TRINITY", "Cognicao e alinhamento"},
    {"ΣΔΩ", "Kernel de estrategia"},
    {"VQF", "Qualidade e verificacao"},
    {"SSM_MATRIX", "Matriz estruturada"}
};

static const Module layer3_modules[] = {
    {"SCAN_ENGINE", "Descoberta de arquivos"},
    {"HASH_ENGINE", "Digest SHA3"},
    {"FILTER_ENGINE", "Filtros e validacao"},
    {"PATH_ENGINE", "Normalizacao de caminho"},
    {"STAT_ENGINE", "Coleta de metadados"}
};

static const Module layer4_modules[] = {
    {"REPORT_ENGINE", "Relatorios markdown"},
    {"JSON_ENGINE", "Indices JSON"},
    {"OPPORTUNITY_ENGINE", "Mapa de oportunidades"},
    {"ARCH_ENGINE", "Arquitetura em camadas"},
    {"SUMMARY_ENGINE", "Resumo executivo"}
};

static const Module layer5_modules[] = {
    {"ERROR_GUARD", "Tratamento de erro"},
    {"IO_GUARD", "Protecao de IO"},
    {"HASH_GUARD", "Consistencia de hash"},
    {"LIMIT_GUARD", "Limites e quotas"},
    {"POLICY_GUARD", "Politicas e etica"}
};

static const Module layer6_modules[] = {
    {"CLI_GATE", "Interface de linha"},
    {"CONFIG_GATE", "Configuração"},
    {"EXPORT_GATE", "Exportacao"},
    {"STATE_GATE", "Estado e contadores"},
    {"TRACE_GATE", "Observabilidade"}
};

static const Module layer7_modules[] = {
    {"HARMONY_LAYER", "Coexistencia harmoniosa"},
    {"PHASE_LAYER", "Ciclos de fase"},
    {"ETHIC_LAYER", "Amor e governanca"}
};

static const Layer layers[7] = {
    {"Camada 1 - Identidade", layer1_modules, sizeof(layer1_modules) / sizeof(layer1_modules[0])},
    {"Camada 2 - Vetores", layer2_modules, sizeof(layer2_modules) / sizeof(layer2_modules[0])},
    {"Camada 3 - Núcleo", layer3_modules, sizeof(layer3_modules) / sizeof(layer3_modules[0])},
    {"Camada 4 - Relatorios", layer4_modules, sizeof(layer4_modules) / sizeof(layer4_modules[0])},
    {"Camada 5 - Guardas", layer5_modules, sizeof(layer5_modules) / sizeof(layer5_modules[0])},
    {"Camada 6 - Interface", layer6_modules, sizeof(layer6_modules) / sizeof(layer6_modules[0])},
    {"Camada 7 - Harmonia", layer7_modules, sizeof(layer7_modules) / sizeof(layer7_modules[0])}
};

static const PipelineStage pipeline_stages[] = {
    {"BOOTSTRAP", "Inicializa contexto e valida configuracoes"},
    {"DISCOVERY", "Navega a arvore e coleta candidatos"},
    {"FILTER", "Aplica regras de extensao e limites"},
    {"METADATA", "Captura estatisticas e tamanho"},
    {"HASHING", "Gera SHA3 quando habilitado"},
    {"INDEX", "Escreve entrada JSON"},
    {"REPORT", "Escreve entrada Markdown"},
    {"SUMMARY", "Consolida metadados e metrics"}
};

static const StageResponsibility pipeline_responsibilities[] = {
    {"BOOTSTRAP", "CONFIG_GATE", "Carregar defaults, flags e base path", "Config efetiva"},
    {"DISCOVERY", "SCAN_ENGINE", "Percorrer diretorios e identificar candidatos", "Lista de caminhos"},
    {"FILTER", "FILTER_ENGINE", "Aplicar extensoes, hidden, depth e size", "Candidatos filtrados"},
    {"METADATA", "STAT_ENGINE", "Extrair tamanho, tipo e erros", "Metadados basicos"},
    {"HASHING", "HASH_ENGINE", "Gerar SHA3 quando habilitado", "Digest SHA3"},
    {"INDEX", "JSON_ENGINE", "Persistir registros no JSON", "Indice JSON"},
    {"REPORT", "REPORT_ENGINE", "Persistir linhas Markdown", "Relatorio MD"},
    {"SUMMARY", "SUMMARY_ENGINE", "Consolidar estatisticas finais", "Sumario executivo"}
};

static void print_usage(const char *prog) {
    printf("Uso: %s [opcoes]\n", prog);
    printf("  --base <path>          Diretorio base (padrao .)\n");
    printf("  --json <path>          Saida JSON (padrao RAFAELIA_CYCLE_INDEX.json)\n");
    printf("  --md <path>            Saida Markdown (padrao RAFAELIA_CYCLE_REPORT.md)\n");
    printf("  --include-hidden       Inclui arquivos ocultos\n");
    printf("  --follow-symlinks      Segue links simbolicos\n");
    printf("  --max-depth <n>         Profundidade maxima (padrao ilimitado)\n");
    printf("  --max-size <bytes>     Tamanho maximo (padrao ilimitado)\n");
    printf("  --extensions <list>    Lista de extensoes separadas por virgula\n");
    printf("  --no-hash              Desativa SHA3\n");
    printf("  --no-architecture      Remove matriz arquitetural\n");
    printf("  --no-opportunities     Remove catalogo de oportunidades\n");
    printf("  --no-pipeline          Remove pipeline de orquestracao\n");
    printf("  --no-responsibilities  Remove matriz de responsabilidades\n");
    printf("  --help                 Exibe esta ajuda\n");
}

static int has_suffix(const char *name, const char *suffix) {
    size_t name_len = strlen(name);
    size_t suffix_len = strlen(suffix);
    if (suffix_len > name_len) return 0;
    return strcmp(name + name_len - suffix_len, suffix) == 0;
}

static int has_valid_ext(const char *name, const Config *cfg) {
    for (size_t i = 0; i < cfg->ext_count; i++) {
        if (has_suffix(name, cfg->exts[i])) return 1;
    }
    return 0;
}

static int is_hidden_name(const char *name) {
    return name[0] == '.';
}

static void sha3_file(const char *path, char *output, size_t output_size) {
    unsigned char hash[32];
    unsigned char buffer[4096];
    EVP_MD_CTX *ctx = EVP_MD_CTX_new();
    FILE *f = fopen(path, "rb");
    if (!ctx || !f) {
        if (f) fclose(f);
        snprintf(output, output_size, "ERROR");
        if (ctx) EVP_MD_CTX_free(ctx);
        return;
    }

    EVP_DigestInit_ex(ctx, EVP_sha3_256(), NULL);
    size_t n;
    while ((n = fread(buffer, 1, sizeof(buffer), f)) > 0) {
        EVP_DigestUpdate(ctx, buffer, n);
    }

    EVP_DigestFinal_ex(ctx, hash, NULL);
    EVP_MD_CTX_free(ctx);
    fclose(f);

    for (int i = 0; i < 32; i++) {
        snprintf(output + i * 2, output_size - (size_t)(i * 2), "%02x", hash[i]);
    }
}

static void write_json_entry(FILE *json_out, int *first_json, const char *path, long size,
                             const char *hash) {
    if (!*first_json) fprintf(json_out, ",\n");
    *first_json = 0;
    fprintf(json_out, "  {\"path\": \"%s\", \"size\": %ld, \"sha3_256\": \"%s\"}",
            path, size, hash);
}

static void write_md_entry(FILE *md_out, const char *path, long size, const char *hash,
                           int hash_enabled) {
    if (hash_enabled) {
        fprintf(md_out, "- `%s` (%ld bytes) sha3=%.*s…\n", path, size, 16, hash);
    } else {
        fprintf(md_out, "- `%s` (%ld bytes) sha3=desativado\n", path, size);
    }
}

static void scan_dir(const char *base, const Config *cfg, FILE *json_out, FILE *md_out,
                     int *first_json, Stats *stats, int depth) {
    DIR *dir = opendir(base);
    if (!dir) {
        stats->errors++;
        return;
    }

    struct dirent *ent;
    while ((ent = readdir(dir))) {
        if (!strcmp(ent->d_name, ".") || !strcmp(ent->d_name, "..")) continue;
        if (!cfg->include_hidden && is_hidden_name(ent->d_name)) continue;

        char path[MAX_PATH];
        snprintf(path, sizeof(path), "%s/%s", base, ent->d_name);

        struct stat st;
        int stat_result = cfg->follow_symlinks ? stat(path, &st) : lstat(path, &st);
        if (stat_result != 0) {
            stats->errors++;
            continue;
        }

        if (S_ISLNK(st.st_mode) && !cfg->follow_symlinks) {
            stats->files_skipped++;
            continue;
        }

        if (S_ISDIR(st.st_mode)) {
            if (cfg->max_depth >= 0 && depth >= cfg->max_depth) {
                stats->files_skipped++;
                continue;
            }
            scan_dir(path, cfg, json_out, md_out, first_json, stats, depth + 1);
        } else if (S_ISREG(st.st_mode) && has_valid_ext(ent->d_name, cfg)) {
            if (cfg->max_size >= 0 && st.st_size > cfg->max_size) {
                stats->files_skipped++;
                continue;
            }

            char hash[65] = {0};
            if (cfg->hash_enabled) {
                sha3_file(path, hash, sizeof(hash));
                if (strcmp(hash, "ERROR") != 0) {
                    stats->files_hashed++;
                }
            } else {
                snprintf(hash, sizeof(hash), "DISABLED");
            }

            write_json_entry(json_out, first_json, path, st.st_size, hash);
            write_md_entry(md_out, path, st.st_size, hash, cfg->hash_enabled);

            stats->files_indexed++;
            stats->total_bytes += st.st_size;
        }
    }

    closedir(dir);
}

static void parse_extensions(Config *cfg, const char *list) {
    char *copy = strdup(list);
    if (!copy) return;
    char *token = strtok(copy, ",");
    cfg->ext_count = 0;
    cfg->owns_exts = 1;
    while (token && cfg->ext_count < MAX_EXTS) {
        while (*token == ' ') token++;
        char *ext = strdup(token);
        if (!ext) break;
        cfg->exts[cfg->ext_count++] = ext;
        token = strtok(NULL, ",");
    }
    free(copy);
}

static void load_default_extensions(Config *cfg) {
    cfg->ext_count = sizeof(default_exts) / sizeof(default_exts[0]);
    cfg->owns_exts = 0;
    for (size_t i = 0; i < cfg->ext_count; i++) {
        cfg->exts[i] = default_exts[i];
    }
}

static void free_extensions(Config *cfg) {
    if (!cfg->owns_exts) return;
    for (size_t i = 0; i < cfg->ext_count; i++) {
        free((void *)cfg->exts[i]);
    }
    cfg->owns_exts = 0;
}

static void write_architecture(FILE *md_out) {
    fprintf(md_out, "\n## Matriz arquitetural (7 camadas, 33 modulos)\n\n");
    for (size_t i = 0; i < sizeof(layers) / sizeof(layers[0]); i++) {
        const Layer *layer = &layers[i];
        fprintf(md_out, "### %s\n\n", layer->layer_name);
        fprintf(md_out, "| Modulo | Papel |\n| --- | --- |\n");
        for (size_t j = 0; j < layer->module_count; j++) {
            fprintf(md_out, "| %s | %s |\n", layer->modules[j].name, layer->modules[j].role);
        }
        fprintf(md_out, "\n");
    }
}

static void write_pipeline(FILE *md_out) {
    fprintf(md_out, "\n## Pipeline de orquestracao (low level)\n\n");
    fprintf(md_out, "| Etapa | Propósito |\n| --- | --- |\n");
    for (size_t i = 0; i < sizeof(pipeline_stages) / sizeof(pipeline_stages[0]); i++) {
        fprintf(md_out, "| %s | %s |\n", pipeline_stages[i].name, pipeline_stages[i].purpose);
    }
    fprintf(md_out, "\n");
}

static void write_responsibilities(FILE *md_out) {
    fprintf(md_out, "\n## Matriz de responsabilidades (cada etapa tem o que fazer)\n\n");
    fprintf(md_out, "| Etapa | Responsavel | Responsabilidade | Saida |\n| --- | --- | --- | --- |\n");
    for (size_t i = 0; i < sizeof(pipeline_responsibilities) / sizeof(pipeline_responsibilities[0]); i++) {
        fprintf(md_out, "| %s | %s | %s | %s |\n",
                pipeline_responsibilities[i].stage,
                pipeline_responsibilities[i].owner,
                pipeline_responsibilities[i].responsibility,
                pipeline_responsibilities[i].output);
    }
    fprintf(md_out, "\n");
}

static void write_opportunities(FILE *md_out) {
    fprintf(md_out, "\n## Catalogo de oportunidades (42)\n\n");
    for (size_t i = 0; i < 42; i++) {
        fprintf(md_out, "%zu. %s\n", i + 1, opportunities[i]);
    }
    fprintf(md_out, "\n");
}

static void write_summary(FILE *md_out, const Config *cfg, const Stats *stats) {
    fprintf(md_out, "\n## Sumario executivo\n\n");
    fprintf(md_out, "- Base: `%s`\n", cfg->base_path);
    fprintf(md_out, "- Arquivos indexados: %ld\n", stats->files_indexed);
    fprintf(md_out, "- Arquivos com hash: %ld\n", stats->files_hashed);
    fprintf(md_out, "- Arquivos ignorados: %ld\n", stats->files_skipped);
    fprintf(md_out, "- Erros: %ld\n", stats->errors);
    fprintf(md_out, "- Total de bytes: %lld\n", stats->total_bytes);
    fprintf(md_out, "- SHA3 ativo: %s\n", cfg->hash_enabled ? "sim" : "nao");
    fprintf(md_out, "- Modo SSM: matriz arquitetural habilitada\n");
}

int main(int argc, char **argv) {
    Config cfg;
    cfg.base_path = ".";
    cfg.json_path = "RAFAELIA_CYCLE_INDEX.json";
    cfg.md_path = "RAFAELIA_CYCLE_REPORT.md";
    cfg.include_hidden = 0;
    cfg.follow_symlinks = 0;
    cfg.hash_enabled = 1;
    cfg.emit_architecture = 1;
    cfg.emit_opportunities = 1;
    int emit_pipeline = 1;
    int emit_responsibilities = 1;
    cfg.max_depth = -1;
    cfg.max_size = -1;
    load_default_extensions(&cfg);

    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--base") && i + 1 < argc) {
            cfg.base_path = argv[++i];
        } else if (!strcmp(argv[i], "--json") && i + 1 < argc) {
            cfg.json_path = argv[++i];
        } else if (!strcmp(argv[i], "--md") && i + 1 < argc) {
            cfg.md_path = argv[++i];
        } else if (!strcmp(argv[i], "--include-hidden")) {
            cfg.include_hidden = 1;
        } else if (!strcmp(argv[i], "--follow-symlinks")) {
            cfg.follow_symlinks = 1;
        } else if (!strcmp(argv[i], "--max-depth") && i + 1 < argc) {
            cfg.max_depth = atoi(argv[++i]);
        } else if (!strcmp(argv[i], "--max-size") && i + 1 < argc) {
            cfg.max_size = atol(argv[++i]);
        } else if (!strcmp(argv[i], "--extensions") && i + 1 < argc) {
            parse_extensions(&cfg, argv[++i]);
        } else if (!strcmp(argv[i], "--no-hash")) {
            cfg.hash_enabled = 0;
        } else if (!strcmp(argv[i], "--no-architecture")) {
            cfg.emit_architecture = 0;
        } else if (!strcmp(argv[i], "--no-opportunities")) {
            cfg.emit_opportunities = 0;
        } else if (!strcmp(argv[i], "--no-pipeline")) {
            emit_pipeline = 0;
        } else if (!strcmp(argv[i], "--no-responsibilities")) {
            emit_responsibilities = 0;
        } else if (!strcmp(argv[i], "--help")) {
            print_usage(argv[0]);
            return 0;
        } else {
            fprintf(stderr, "Opcao invalida: %s\n", argv[i]);
            print_usage(argv[0]);
            return 1;
        }
    }

    FILE *json_out = fopen(cfg.json_path, "w");
    FILE *md_out = fopen(cfg.md_path, "w");

    if (!json_out || !md_out) {
        fprintf(stderr, "Erro abrindo arquivos de saida: %s\n", strerror(errno));
        if (json_out) fclose(json_out);
        if (md_out) fclose(md_out);
        free_extensions(&cfg);
        return 1;
    }

    Stats stats = {0};
    int first_json = 1;

    fprintf(json_out, "[\n");
    fprintf(md_out, "# RAFAELIA – Cycle Report\n\n");
    fprintf(md_out, "## Files indexed\n\n");

    scan_dir(cfg.base_path, &cfg, json_out, md_out, &first_json, &stats, 0);

    fprintf(json_out, "\n]\n");
    write_summary(md_out, &cfg, &stats);

    if (cfg.emit_architecture) {
        write_architecture(md_out);
    }

    if (emit_pipeline) {
        write_pipeline(md_out);
    }

    if (emit_responsibilities) {
        write_responsibilities(md_out);
    }

    if (cfg.emit_opportunities) {
        write_opportunities(md_out);
    }

    fclose(json_out);
    fclose(md_out);
    free_extensions(&cfg);

    printf("[OK] Generated:\n");
    printf(" - %s\n", cfg.json_path);
    printf(" - %s\n", cfg.md_path);

    return 0;
}
