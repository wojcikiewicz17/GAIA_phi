#include "../headers/omega_nexus.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>

NexusHeader* header_ptr = NULL;
NexusCell* cells_ptr = NULL;
static int nexus_fd = -1;
static size_t file_size = 0;

int nexus_init(const char* filepath, uint64_t capacity) {
    nexus_fd = open(filepath, O_RDWR | O_CREAT, 0644);
    if (nexus_fd == -1) return -1;
    size_t total_sz = sizeof(NexusHeader) + (capacity * sizeof(NexusCell));
    struct stat st; fstat(nexus_fd, &st);
    if (st.st_size == 0) if (ftruncate(nexus_fd, total_sz) == -1) return -1;
    file_size = total_sz;
    void* map = mmap(NULL, total_sz, PROT_READ | PROT_WRITE, MAP_SHARED, nexus_fd, 0);
    if (map == MAP_FAILED) return -1;
    header_ptr = (NexusHeader*)map;
    cells_ptr = (NexusCell*)((char*)map + sizeof(NexusHeader));
    if (st.st_size == 0) { header_ptr->capacity = capacity; header_ptr->count = 0; }
    return 0;
}
int nexus_append(VectorVerb* v, const char* action) {
    if (!header_ptr || header_ptr->count >= header_ptr->capacity) return -1;
    NexusCell* c = &cells_ptr[header_ptr->count];
    c->id = header_ptr->count;
    c->vector[0] = v->data[0]; c->vector[1] = v->data[1]; c->vector[2] = v->data[2];
    strncpy(c->action_tag, action, 31);
    c->confidence = 1.0f;
    header_ptr->count++;
    return 0;
}
void nexus_scan_match(VectorVerb* input, void (*callback)(NexusCell*)) {
    if (!header_ptr) return;
    for (uint64_t i = 0; i < header_ptr->count; i++) {
        NexusCell* c = &cells_ptr[i];
        float dot = (input->data[0] * c->vector[0]) + (input->data[1] * c->vector[1]) + (input->data[2] * c->vector[2]);
        if (dot > 0.85f) callback(c);
    }
}
void nexus_close() { if (header_ptr) munmap(header_ptr, file_size); if (nexus_fd != -1) close(nexus_fd); }
