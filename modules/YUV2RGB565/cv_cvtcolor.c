#include <xtensa/config/core-isa.h>
#include <xtensa/tie/xt_core.h>
#include <xtensa/tie/xt_misc.h>
#include <xtensa/tie/xt_hifi3.h>
#include <xtensa/tie/xt_hifi4.h>
#include "../comm/comp_debug.h"

#define CLOG_LEVEL              CLOG_LEVEL_VBS
#include "venus_log.h"
#define ASSERT(exp, fmt, ...)	do{if(!(exp)){CLOGW("error:"fmt,##__VA_ARGS__);assert(exp);}}while(0)

void cv_cvtcolor_yuv422vyuy_bgr888(const unsigned char* src, unsigned char* dst, unsigned int width, unsigned int height)
{
	int i, j, k;
	ae_int16x4 x0_0, x0_1, y0_0, v0_0, u0_0, xh0_0;
	ae_int32x2 z0_00, z0_01, z0_10, z0_11, z0_20, z0_21;
	ae_int24x2 z0_0, z0_1;
	ae_int16x4* px;
	ae_int24x2* pz;
	ae_int16x4 x256 = AE_MOVDA16(256);
	ae_int16x4 x128 = AE_MOVDA16(128);
	ae_int16x4 x359 = AE_MOVDA16(359);
	ae_int16x4 x183 = AE_MOVDA16(-183);
	ae_int16x4 x444 = AE_MOVDA16(444);
	ae_int16x4 x88 = AE_MOVDA16(-88);
	ae_int16x4 xff = AE_MOVDA16(0xff);
	ae_int32x2 zmask0 = AE_MOVDA32(0xff);
	ae_int32x2 zmask1 = AE_MOVDA32(0xff00);
	ae_int32x2 zmask2 = AE_MOVDA32(0xff0000);
	ae_int32x2 zmax = AE_MOVDA32(0xffff);
	ae_int32x2 zmin = AE_MOVDA32(0x0);

	unsigned int z;
	const unsigned char* yuv_plane = src;
	unsigned char* rgb_plane = dst;

	px = (ae_int16x4*)yuv_plane;
	pz = (ae_int24x2*)rgb_plane;

	// NASSERT(((uintptr_t)src & 0x7) == 0);
	// NASSERT(((uintptr_t)dst & 0x7) == 0);
	// NASSERT((width & 0x3) == 0);

	AE_L16X4_IP(xh0_0, px, 8);
	ae_valign zo_align = AE_ZALIGN64();
	const int max_size = (height*width) >> 2;
	for (int j = 0; j < max_size; j++)
	{
		x0_0 = xh0_0;

		x0_1 = AE_AND16(x0_0, xff);
		y0_0 = AE_SLAA16S(x0_0, -8);
		y0_0 = AE_AND16(y0_0, xff);
		//y0 = AE_MOVINT16X4_FROMINT64((AE_SRLI64(AE_MOVINT64_FROMINT16X4(x0), 8)));

		x0_0 = AE_SEL16_7632(x0_1, x0_1);
		x0_1 = AE_SEL16_5410(x0_1, x0_1);
		v0_0 = AE_SEL16_7531(x0_0, x0_1);
		u0_0 = AE_SEL16_6420(x0_0, x0_1);
		v0_0 = AE_SUB16(v0_0, x128);
		u0_0 = AE_SUB16(u0_0, x128);

		//R
		AE_MUL16X4(z0_00, z0_01, y0_0, x256);
		//z10 = z00; z11 = z01;
		AE_MULA16X4(z0_00, z0_01, v0_0, x359);
		//G
		AE_MUL16X4(z0_10, z0_11, y0_0, x256);
		//z20 = z10; z21 = z11;
		AE_MULA16X4(z0_10, z0_11, v0_0, x183);
		AE_MULA16X4(z0_10, z0_11, u0_0, x88);
		//B
		AE_MUL16X4(z0_20, z0_21, y0_0, x256);
		AE_MULA16X4(z0_20, z0_21, u0_0, x444);
		AE_L16X4_IP(xh0_0, px, 8);
#if 1
		z0_00 = AE_MAX32(z0_00, zmin);
		z0_00 = AE_MIN32(z0_00, zmax);
		z0_01 = AE_MAX32(z0_01, zmin);
		z0_01 = AE_MIN32(z0_01, zmax);

		z0_10 = AE_MAX32(z0_10, zmin);
		z0_10 = AE_MIN32(z0_10, zmax);
		z0_11 = AE_MAX32(z0_11, zmin);
		z0_11 = AE_MIN32(z0_11, zmax);

		z0_20 = AE_MAX32(z0_20, zmin);
		z0_20 = AE_MIN32(z0_20, zmax);
		z0_21 = AE_MAX32(z0_21, zmin);
		z0_21 = AE_MIN32(z0_21, zmax);
#endif 
		//L->H:BGR0
		z0_00 = AE_AND32(AE_SLAA32S(z0_00, 8), zmask2);//H ((>>8)<<16)
		z0_10 = AE_AND32(z0_10, zmask1); //((>>8)<<8)
		z0_20 = AE_AND32(AE_SLAA32S(z0_20, -8), zmask0);//L
		z0_00 = AE_OR32(z0_00, AE_OR32(z0_10, z0_20));
		z0_0 = AE_MOVINT24X2_FROMF32X2(z0_00);
		AE_SA24X2_IP(z0_0, zo_align, pz);

		z0_01 = AE_AND32(AE_SLAA32S(z0_01, 8), zmask2);
		z0_11 = AE_AND32(z0_11, zmask1);
		z0_21 = AE_AND32(AE_SLAA32S(z0_21, -8), zmask0);
		z0_01 = AE_OR32(z0_01, AE_OR32(z0_11, z0_21));
		z0_1 = AE_MOVINT24X2_FROMF32X2(z0_01);
		AE_SA24X2_IP(z0_1, zo_align, pz);
	}
	AE_SA64POS_FP(zo_align, pz);
}


void cv_cvtcolor_yuv422vyuy_bgr888_trans(const unsigned char* src, unsigned char* dst, unsigned int width, unsigned int height)
{
	int i, j, k;
	const unsigned char *p_p0_s, *p_p1_s;
	unsigned char *p_p0_d, *p_p1_d;
	const unsigned char *p_p0_s_4x2, *p_p1_s_4x2;
	unsigned char *p_p0_d_4x3, *p_p1_d_4x3;

	ae_int16x4 x0_0, x0_1, y0_0, v0_0, u0_0, xh0_0;
	ae_int32x2 z0_00, z0_01, z0_10, z0_11, z0_20, z0_21;
	ae_int24x2 z0_0, z0_1;
	ae_int16x4 x1_0, x1_1, y1_0, v1_0, u1_0, xh1_0;
	ae_int32x2 z1_00, z1_01, z1_10, z1_11, z1_20, z1_21;
	ae_int24x2 z1_0, z1_1;
	ae_int16x4 *px0, *px1;
	ae_int24x2 *pz0, *pz1;
	ae_int16x4 x256 = AE_MOVDA16(256);
	ae_int16x4 x128 = AE_MOVDA16(128);
	ae_int16x4 x359 = AE_MOVDA16(359);
	ae_int16x4 x183 = AE_MOVDA16(-183);
	ae_int16x4 x444 = AE_MOVDA16(444);
	ae_int16x4 x88 = AE_MOVDA16(-88);
	ae_int16x4 xff = AE_MOVDA16(0xff);
	ae_int32x2 zmask0 = AE_MOVDA32(0xff);
	ae_int32x2 zmask1 = AE_MOVDA32(0xff00);
	ae_int32x2 zmask2 = AE_MOVDA32(0xff0000);
	ae_int32x2 zmax = AE_MOVDA32(0xffff);
	ae_int32x2 zmin = AE_MOVDA32(0x0);

	unsigned int z;
	const unsigned char* yuv_plane = src;
	unsigned char* rgb_plane = dst;

	// NASSERT(((uintptr_t)src & 0x7) == 0);
	// NASSERT(((uintptr_t)dst & 0x7) == 0);
	// NASSERT((width & 0x3) == 0);
	// NASSERT((height & 0x1) == 0);
	
	const int max_height = height >> 1;
	const int max_width = width >> 2;
	for (int i = 0; i < max_height; i++)
	{
		p_p0_s = src + (i << 1) * (width << 1);
		p_p1_s = src + ((i << 1) + 1) * (width << 1);

		p_p0_d = dst + (i << 1) * width * 3;
		p_p1_d = dst + ((i << 1) + 1) * width * 3;

		ae_valign zo_align0 = AE_ZALIGN64();
		ae_valign zo_align1 = AE_ZALIGN64();

		px0 = (ae_int16x4*)p_p0_s;
		px1 = (ae_int16x4*)p_p1_s;
		pz0 = (ae_int24x2*)p_p0_d;
		pz1 = (ae_int24x2*)p_p1_d;

		//AE_L16X4_IP(xh0_0, px0, 8);
		//AE_L16X4_IP(xh1_0, px1, 8);

		for (int j = 0; j < max_width; j++)
		{
			AE_L16X4_IP(x0_0, px0, 8);
			AE_L16X4_IP(x1_0, px1, 8);
			//x0_0 = xh0_0;
			//x1_0 = xh1_0;

			y0_0 = AE_SLAA16S(x0_0, -8);
			y0_0 = AE_AND16(y0_0, xff);
			y1_0 = AE_SLAA16S(x1_0, -8);
			y1_0 = AE_AND16(y1_0, xff);
			
			v0_0 = AE_AND16(x0_0, xff);
			u0_0 = AE_AND16(x1_0, xff);

			v0_0 = AE_SUB16(v0_0, x128);
			u0_0 = AE_SUB16(u0_0, x128);

			//plane0
			//R
			AE_MUL16X4(z0_00, z0_01, y0_0, x256);
			//z10 = z00; z11 = z01;
			AE_MULA16X4(z0_00, z0_01, v0_0, x359);
			//G
			AE_MUL16X4(z0_10, z0_11, y0_0, x256);
			//z20 = z10; z21 = z11;
			AE_MULA16X4(z0_10, z0_11, v0_0, x183);
			AE_MULA16X4(z0_10, z0_11, u0_0, x88);
			//B
			AE_MUL16X4(z0_20, z0_21, y0_0, x256);
			AE_MULA16X4(z0_20, z0_21, u0_0, x444);

			//AE_L16X4_IP(xh0_0, px0, 8);

#if 1
			z0_00 = AE_MAX32(z0_00, zmin);
			z0_00 = AE_MIN32(z0_00, zmax);
			z0_01 = AE_MAX32(z0_01, zmin);
			z0_01 = AE_MIN32(z0_01, zmax);

			z0_10 = AE_MAX32(z0_10, zmin);
			z0_10 = AE_MIN32(z0_10, zmax);
			z0_11 = AE_MAX32(z0_11, zmin);
			z0_11 = AE_MIN32(z0_11, zmax);

			z0_20 = AE_MAX32(z0_20, zmin);
			z0_20 = AE_MIN32(z0_20, zmax);
			z0_21 = AE_MAX32(z0_21, zmin);
			z0_21 = AE_MIN32(z0_21, zmax);
#endif 
			//L->H:BGR0
			z0_00 = AE_AND32(AE_SLAA32S(z0_00, 8), zmask2);//H ((>>8)<<16)
			z0_10 = AE_AND32(z0_10, zmask1); //((>>8)<<8)
			z0_20 = AE_AND32(AE_SLAA32S(z0_20, -8), zmask0);//L
			z0_00 = AE_OR32(z0_00, AE_OR32(z0_10, z0_20));
			z0_0 = AE_MOVINT24X2_FROMF32X2(z0_00);
			AE_SA24X2_IP(z0_0, zo_align0, pz0);

			z0_01 = AE_AND32(AE_SLAA32S(z0_01, 8), zmask2);
			z0_11 = AE_AND32(z0_11, zmask1);
			z0_21 = AE_AND32(AE_SLAA32S(z0_21, -8), zmask0);
			z0_01 = AE_OR32(z0_01, AE_OR32(z0_11, z0_21));
			z0_1 = AE_MOVINT24X2_FROMF32X2(z0_01);
			AE_SA24X2_IP(z0_1, zo_align0, pz0);

			//plane1
			//R
			AE_MUL16X4(z0_00, z0_01, y1_0, x256);
			//z10 = z00; z11 = z01;
			AE_MULA16X4(z0_00, z0_01, v0_0, x359);
			//G
			AE_MUL16X4(z0_10, z0_11, y1_0, x256);
			//z20 = z10; z21 = z11;
			AE_MULA16X4(z0_10, z0_11, v0_0, x183);
			AE_MULA16X4(z0_10, z0_11, u0_0, x88);
			//B
			AE_MUL16X4(z0_20, z0_21, y1_0, x256);
			AE_MULA16X4(z0_20, z0_21, u0_0, x444);


			//AE_L16X4_IP(xh1_0, px1, 8);

#if 1
			z0_00 = AE_MAX32(z0_00, zmin);
			z0_00 = AE_MIN32(z0_00, zmax);
			z0_01 = AE_MAX32(z0_01, zmin);
			z0_01 = AE_MIN32(z0_01, zmax);

			z0_10 = AE_MAX32(z0_10, zmin);
			z0_10 = AE_MIN32(z0_10, zmax);
			z0_11 = AE_MAX32(z0_11, zmin);
			z0_11 = AE_MIN32(z0_11, zmax);

			z0_20 = AE_MAX32(z0_20, zmin);
			z0_20 = AE_MIN32(z0_20, zmax);
			z0_21 = AE_MAX32(z0_21, zmin);
			z0_21 = AE_MIN32(z0_21, zmax);
#endif 
			//L->H:BGR0
			z0_00 = AE_AND32(AE_SLAA32S(z0_00, 8), zmask2);//H ((>>8)<<16)
			z0_10 = AE_AND32(z0_10, zmask1); //((>>8)<<8)
			z0_20 = AE_AND32(AE_SLAA32S(z0_20, -8), zmask0);//L
			z0_00 = AE_OR32(z0_00, AE_OR32(z0_10, z0_20));
			z0_0 = AE_MOVINT24X2_FROMF32X2(z0_00);
			AE_SA24X2_IP(z0_0, zo_align1, pz1);

			z0_01 = AE_AND32(AE_SLAA32S(z0_01, 8), zmask2);
			z0_11 = AE_AND32(z0_11, zmask1);
			z0_21 = AE_AND32(AE_SLAA32S(z0_21, -8), zmask0);
			z0_01 = AE_OR32(z0_01, AE_OR32(z0_11, z0_21));
			z0_1 = AE_MOVINT24X2_FROMF32X2(z0_01);
			AE_SA24X2_IP(z0_1, zo_align1, pz1);
		}

		AE_SA64POS_FP(zo_align0, pz0);
		AE_SA64POS_FP(zo_align1, pz1);

	}
}