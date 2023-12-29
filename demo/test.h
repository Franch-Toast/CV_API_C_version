#ifndef TEST_H
#define TEST_H

#include "stdint.h"


void load_bin_file(const char *file, int8_t **ptr, uint64_t *size);
void save_bin_file(const char *file, int8_t *ptr, int32_t size);
void dump_uint8(const char *name, uint8_t *data, int channel, int height, int width, int width_begin, int width_end, int fixq, char format);
// void dump_int8(const char *name, int8_t *data, int32_t channel, int32_t height, int32_t width, int32_t width_begin, int32_t width_end, int32_t fixq, char format);

#endif