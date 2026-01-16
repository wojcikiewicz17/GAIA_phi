#include "../headers/omega_gui.h"
#include <stdio.h>
void gui_clear() { printf("\033[2J\033[H"); }
void gui_move(int x, int y) { printf("\033[%d;%dH", y, x); }
void gui_draw_box(int x, int y, int w, int h, const char* title) {
    gui_move(x, y); printf("┌"); for(int i=0;i<w-2;i++) printf("─"); printf("┐");
    for(int i=1;i<h-1;i++) { gui_move(x,y+i); printf("│"); gui_move(x+w-1,y+i); printf("│"); }
    gui_move(x,y+h-1); printf("└"); for(int i=0;i<w-2;i++) printf("─"); printf("┘");
    if(title) { gui_move(x+2,y); printf(" %s ", title); }
}
void gui_render_radar(VectorVerb* cur, NexusHeader* h, NexusCell* c) {
    uint64_t limit = (h->count > 500) ? 500 : h->count;
    for(uint64_t i=0;i<limit;i++) {
        int sx = 2 + (int)(c[i].vector[0] * (SCREEN_W-4));
        int sy = 2 + (int)(c[i].vector[1] * (SCREEN_H-4));
        gui_move(sx, sy); printf(".");
    }
    int cx = 2 + (int)(cur->data[0] * (SCREEN_W-4));
    int cy = 2 + (int)(cur->data[1] * (SCREEN_H-4));
    gui_move(cx, cy); printf("+");
}
