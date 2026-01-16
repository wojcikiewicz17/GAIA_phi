#ifndef OMEGA_GUI_H
#define OMEGA_GUI_H
#include "omega_protocol.h"
#include "omega_nexus.h"
#define SCREEN_W 80
#define SCREEN_H 24
void gui_clear();
void gui_move(int x, int y);
void gui_draw_box(int x, int y, int w, int h, const char* title);
void gui_render_radar(VectorVerb* current_input, NexusHeader* header, NexusCell* cells);
#endif
