#include "hifi_cv_sim/NatureDSP_CV_math.h"

#define CLIP_INT8(x)  (x) < 0 ? 0 : ((x) > 255 ? 255 : (x))
//#define CLIP_INT8(x) x

static void yuv422vyuy_bgr888(unsigned char Y, unsigned char Cr, unsigned char Cb, unsigned char* R, unsigned char* G, unsigned char*B)
{
#if 1
	// 	*R = Y + ((359 * (Cr - 128)) >> 8);
	// 	*G = Y - ((183 * (Cr - 128) - 88 * (Cb - 128)) >> 8);
	// 	*B = Y + ((444 * (Cb - 128)) >> 8);
	*R = CLIP_INT8((256 * Y + 359 * (Cr - 128)) >> 8);
	*G = CLIP_INT8((256 * Y - 183 * (Cr - 128) - 88 * (Cb - 128)) >> 8);
	*B = CLIP_INT8((256 * Y + 444 * (Cb - 128)) >> 8);

	// 	*R = Y + 359 * Cr/256 - 359 * 128/256;
	// 	*G = Y - 183 * Cr/256 + 183 * 128/256 - 88 * Cb/256 + 88*128/256;
	// 	*B = Y + 444 * Cb/256 - (444 * 128)/256;
	// 	*R = Y + ((359 * Cr) >> 8) - 178;
	// 	*G = Y - ((183 * Cr) >> 8) - ((88 * Cb) >> 8) + 136;
	// 	*B = Y + ((444 * Cb) >> 8) - 222;
	//opencv
#else
	//opencv
	*R = Y + 1.403*(Cr - 128);
	*G = Y - 0.714*(Cr - 128) - 0.344*(Cb - 128);
	*B = Y + 1.733*(Cb - 128);
#endif
}

void HIFI_SIM(cv_cvtcolor_yuv422vyuy_bgr888)(const unsigned char* src, unsigned char* dst, unsigned int width, unsigned int height)
{
	int i, j, k;
	const unsigned char* yuv_plane = src;
	unsigned char* rgb_plane = dst;
	for (int i = 0; i < height*(width >> 1); i++)
	{
		unsigned char v = yuv_plane[0];
		unsigned char y1 = yuv_plane[1];
		unsigned char u = yuv_plane[2];
		unsigned char y2 = yuv_plane[3];

		yuv422vyuy_bgr888(y1, v, u, rgb_plane + 2, rgb_plane + 1, rgb_plane + 0);
		rgb_plane += 3;
		yuv422vyuy_bgr888(y2, v, u, rgb_plane + 2, rgb_plane + 1, rgb_plane + 0);
		rgb_plane += 3;
		yuv_plane += 4;
	}
}

void HIFI_SIM(cv_transpose16x16_fast)(int16_t  *  y, const int16_t*     x, int M, int N)
{
	int i, j;
	for (i = 0; i < M; i++)
	{
		for (j = 0; j < N; j++)
		{
			y[j*M + i] = x[i*N + j];
		}
	}
}

void HIFI_SIM(cv_cvtcolor_yuv422vyuy_bgr888_trans)(const unsigned char* src, unsigned char* dst, unsigned int width, unsigned int height)
{
	int i, j, k;
	const unsigned char *p_p0_s, *p_p1_s;
	unsigned char *p_p0_d, *p_p1_d;
	const unsigned char *p_p0_s_4x2, *p_p1_s_4x2;
	unsigned char *p_p0_d_4x3, *p_p1_d_4x3;

	for (int i = 0; i < (height >> 1); i++)
	{
		p_p0_s = src + (i * 2) * width * 2;
		p_p1_s = src + (i * 2 + 1) * width * 2;

		p_p0_d = dst + (i * 2) * width * 3;
		p_p1_d = dst + (i * 2 + 1) * width * 3;
		for (int j = 0; j < (width >> 2); j++)
		{
			p_p0_s_4x2 = p_p0_s + j * 4 * 2; //vy
			p_p1_s_4x2 = p_p1_s + j * 4 * 2; //uy

			p_p0_d_4x3 = p_p0_d + j * 4 * 3; //bgr
			p_p1_d_4x3 = p_p1_d + j * 4 * 3; //bgr

			for (int k = 0; k < 4; k++)
			{
				unsigned char r, g, b;
				unsigned char y0 = p_p0_s_4x2[2 * k + 1];
				unsigned char y1 = p_p1_s_4x2[2 * k + 1];
				unsigned char v = p_p0_s_4x2[2 * k];
				unsigned char u = p_p1_s_4x2[2 * k];

				yuv422vyuy_bgr888(y0, v, u, &r, &g, &b);

				p_p0_d_4x3[3 * k + 0] = b;
				p_p0_d_4x3[3 * k + 1] = g;
				p_p0_d_4x3[3 * k + 2] = r;

				yuv422vyuy_bgr888(y1, v, u, &r, &g, &b);

				p_p1_d_4x3[3 * k + 0] = b;
				p_p1_d_4x3[3 * k + 1] = g;
				p_p1_d_4x3[3 * k + 2] = r;
			}
		}
	}
}
