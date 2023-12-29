#ifndef __CV_CVTCOLOR_H__
#define __CV_CVTCOLOR_H__

void cv_cvtcolor_yuv422vyuy_bgr888(const unsigned char* src, unsigned char* dst, unsigned int width, unsigned int height);
void cv_cvtcolor_yuv422vyuy_bgr888_trans(const unsigned char* src, unsigned char* dst, unsigned int width, unsigned int height);

#endif
