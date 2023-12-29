
#include <stdio.h>
#include <stdlib.h>
#include "bmp.h"
#include "ls_cutline_type.h"
#include "istitch_type.h"

// #define linux

#if !(defined(WIN32) || defined(linux))
	#define CASTOR (1)
#else
	#define CASTOR (0)
#endif

#if !CASTOR
int parse_bmp(const char *data,ISTITCH_FRAME *frame)
{
	//memset(bmp_info, 0x00, sizeof(BmpInfo));
	unsigned short bfType = *(unsigned short*)data;
	if (bfType != 0x4D42)
	{
		printf("this is not bmp file!\n");
		return -1;
	}

	BITMAPFILEHEADER *bmp_file_header = NULL;
	BITMAPINFOHEADER *bmp_info_header = NULL;

	const char *p = data + sizeof(bfType);

	bmp_file_header = (BITMAPFILEHEADER *)p;
	p += sizeof(BITMAPFILEHEADER);
	
	bmp_info_header = (BITMAPINFOHEADER *)p;
	p += sizeof(BITMAPINFOHEADER);

	int pixel_info_num = 0;
	int width =bmp_info_header->biWidth;
	int height = bmp_info_header->biHeight;
	int bitCount = bmp_info_header->biBitCount;

	frame->w = width;
	frame->h = height;

	frame->step = bitCount * width;
	switch (bitCount)
	{
	case 8:
		pixel_info_num = 256;
		frame->fmt = ISTITCH_PIX_FMT_GRAY8;
		break;
	case 24:
		pixel_info_num = 0;
		frame->fmt = ISTITCH_PIX_FMT_BGR888;
		break;
	default:
		printf("format not suport!\n");
		return -2;
		break;
	}

	unsigned char *img_data = data + bmp_file_header->bfOffBits;

	int byte_per_line = (((width * bitCount) + 31) / 32) * 4;
	int byte_per_pixel = bitCount / 8;
	int data_len = width * height * byte_per_pixel;
	unsigned char *buf = (unsigned char *)malloc(data_len);

	frame->data = buf;

	for (int i = 0; i < height; i++)
	{
		for (int j = 0; j < width * byte_per_pixel; j++)
		{
			buf[i * width + j] = img_data[(height - i - 1) * byte_per_line + j];
		}
	}
	return data_len;

}


int save_bmp(const char *name, int fmt,unsigned char  *data,int width,int height)
{
	FILE *fp = fopen(name, "wb");
	ivAssert(fp != NULL);

	unsigned short bfType = 0x4D42;
	int write_bytes = fwrite(&bfType, sizeof(unsigned short), 1, fp);

	BITMAPFILEHEADER bmp_file_header;
	BITMAPINFOHEADER bmp_info_header;
	memset(&bmp_file_header, 0x00, sizeof(BITMAPFILEHEADER));
	memset(&bmp_info_header, 0x00, sizeof(BITMAPINFOHEADER));


	unsigned int bitCount = 0;
	int pix_info_num = 0;
	switch (fmt)
	{
	case ISTITCH_PIX_FMT_GRAY8:
		bitCount = 8;
		pix_info_num = 256;
		break;
	case ISTITCH_PIX_FMT_BGR888:
	case ISTITCH_PIX_FMT_RGB888:
		bitCount = 24;
		pix_info_num = 0;
		break;
	default:
		printf("error fmt!\n");
		return -1;
	}

	int byte_per_line = (((width * bitCount) + 31) / 32) * 4;
	int byte_per_pixel = bitCount / 8;
	
	int data_len = byte_per_line * height *byte_per_pixel;
	
	int header_len = sizeof(unsigned short) + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + pix_info_num * sizeof(PixelInfo);
	int file_len = data_len + header_len;

	bmp_file_header.bfSize = file_len;
	bmp_file_header.bfOffBits = header_len;
	bmp_file_header.bfReserved1 = 0;
	bmp_file_header.bfReserved2 = 0;



	write_bytes += fwrite(&bmp_file_header, sizeof(BITMAPFILEHEADER), 1, fp);

	bmp_info_header.biBitCount = bitCount;
	bmp_info_header.biWidth = width;
	bmp_info_header.biHeight = height;
	bmp_info_header.biSize = sizeof(BITMAPINFOHEADER);
	bmp_info_header.biPlanes = 1;
	bmp_info_header.biCompression = 0;
	bmp_info_header.biSizeImage = bmp_file_header.bfSize - bmp_file_header.bfOffBits;
	bmp_info_header.biXPelsPerMeter = 0;
	bmp_info_header.biYPelsPerMeter = 0;
	bmp_info_header.biClrUsed = 0;
	bmp_info_header.biClrImportant = 0;
	write_bytes += fwrite(&bmp_info_header, sizeof(BITMAPINFOHEADER), 1, fp);

	PixelInfo pixel_info = { 0 };
	for (int i = 0; i < pix_info_num; i++)
	{
		pixel_info.rgbBlue = i;
		pixel_info.rgbGreen = i;
		pixel_info.rgbRed = i;
		pixel_info.rgbReserved = 0;

		write_bytes += fwrite(&pixel_info, sizeof(PixelInfo), 1, fp);
	}

	unsigned char *pdata = data;
	unsigned char *pCurdata = pdata;
	unsigned char fill_data[1] = { 0 };
	for (int i = 0; i < height; i++)
	{
		for (int j = 0; j < width * byte_per_pixel; j++)
		{
			pCurdata = pdata + (height - 1 - i)*width + j;
			write_bytes += fwrite(pCurdata, sizeof(unsigned char), 1, fp);
		}
		for (int j = width * byte_per_pixel; j < byte_per_line; j++)
		{
			write_bytes += fwrite(&fill_data, sizeof(unsigned char), 1, fp);
		}
	}

	
	if (fp != NULL)
		fclose(fp);
	return write_bytes;
}
#endif

//内存需从外部分配好
int parse_bmp_from_mem(const char *data, ISTITCH_FRAME *frame)
{
	//memset(bmp_info, 0x00, sizeof(BmpInfo));
	unsigned short bfType = *(unsigned short*)data;
	if (bfType != 0x4D42)
	{
		printf("this is not bmp file!\n");
		return -1;
	}

	BITMAPFILEHEADER *bmp_file_header = NULL;
	BITMAPINFOHEADER *bmp_info_header = NULL;

	const char *p = data + sizeof(bfType);

	bmp_file_header = (BITMAPFILEHEADER *)p;
	p += sizeof(BITMAPFILEHEADER);

	bmp_info_header = (BITMAPINFOHEADER *)p;
	p += sizeof(BITMAPINFOHEADER);

	int pixel_info_num = 0;
	int width = bmp_info_header->biWidth;
	int height = bmp_info_header->biHeight;
	int bitCount = bmp_info_header->biBitCount;

	frame->w = width;
	frame->h = height;

	frame->step = bitCount * width;
	switch (bitCount)
	{
	case 8:
		pixel_info_num = 256;
		frame->fmt = ISTITCH_PIX_FMT_GRAY8;
		break;
	case 24:
		pixel_info_num = 0;
		frame->fmt = ISTITCH_PIX_FMT_BGR888;
		break;
	default:
		printf("format not suport!\n");
		return -2;
		break;
	}

	unsigned char *img_data = (unsigned char *)data + bmp_file_header->bfOffBits;

	int byte_per_line = (((width * bitCount) + 31) / 32) * 4;
	int byte_per_pixel = bitCount / 8;
	int data_len = width * height * byte_per_pixel;
	//unsigned char *buf = (unsigned char *)malloc(data_len);

	unsigned char * buf = frame->data;

	for (int i = 0; i < height; i++)
	{
		for (int j = 0; j < width * byte_per_pixel; j++)
		{
			buf[i * width + j] = img_data[(height - i - 1) * byte_per_line + j];
		}
	}
	return bmp_file_header->bfSize;

}
