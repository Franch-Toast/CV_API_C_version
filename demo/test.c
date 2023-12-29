#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "engine_utils/cv_utils.h"
#include "engine_utils/common.h"
#include "bmp.h"
#include "test.h"

/*  测试宏定义开关  */

#define ROTATE_180_TEST 		// 旋转180°
#define FLIP_LEFT_RIGHT_TEST	// 左右翻转
#define PAD_0_TEST				// 边缘填充(mode = 0)
#define MIN_BLUR_TEST			// 最小值滤波


inline void load_bin_file(const char *file, int8_t **ptr, uint64_t *size) 
{
    FILE *fp = fopen(file, "rb");

    fseek(fp, 0 ,SEEK_END);
    *size = ftell(fp);
    fseek(fp, 0 ,SEEK_SET);
    *ptr = (int8_t *)malloc(*size);
    fread(*ptr, *size, 1, fp);
    fclose(fp);
}

inline void save_bin_file(const char *file, int8_t *ptr, int32_t size)
{
	FILE *fp = fopen(file, "ab+");

	fwrite(ptr, size, 1, fp);

	fclose(fp);
}

inline void dump_uint8(const char *name, uint8_t *data, int channel, int height, int width, int width_begin, int width_end, int fixq, char format)
{
	//cwh
	//width大小包含了width_history
	FILE* fp;
	int c, h, w;
	float scale = (float)(1 << fixq);

	fp = fopen(name, "w");

	for (c = 0; c < channel; c++)
	{
		for (h = 0; h < height; h++)
		{
			for (w = width_begin; w < width_end; w++)
			{
				if ('u' == format)
                {
					if (w == width_end -1)
                    	fprintf(fp, "%u\n", data[c * width * height + h * width + w]);
					else
                    	fprintf(fp, "%u ", data[c * width * height + h * width + w]);
                }
                else if ('d' == format)
				{
					if (w == width_end -1)
                    	fprintf(fp, "%d\n", data[c * width * height + h * width + w]);
					else
						fprintf(fp, "%d\n", data[c * width * height + h * width + w]);
				}
				else if ('f' == format)
				{
					if (w == width_end -1)
                    	fprintf(fp, "%f\n", data[c * width * height + h * width + w] / scale);
					else					
						fprintf(fp, "%f\n", data[c * width * height + h * width + w] / scale);
				}
			}
			// fprintf(fp, "\n");
		}
		// fprintf(fp, "\n");
	}

	fclose(fp);
}

int32_t main()
{
    int8_t *input_data = NULL;
    uint64_t input_size;
    load_bin_file("ori_img.bin", &input_data, &input_size);
    int32_t height = 1904;
    int32_t width = 1080;
    int32_t channel = 3;

    tData src;
	// src[0] = malloc(sizeof(tData)*3);
    src.shape_.ndim_ = 3;
    src.shape_.dims_[0] = height;
    src.shape_.dims_[1] = width;
    src.shape_.dims_[2] = channel;
    src.dptr_ = (uint8_t *)input_data;

	// 输出原始图像数据
	dump_uint8("ori_img.txt", (uint8_t *)input_data, src.shape_.dims_[0], src.shape_.dims_[1], src.shape_.dims_[2], 0, src.shape_.dims_[2], 1, 'u');

	uint8_t *out_data;
	int32_t ret;
	tData dst;
	int32_t *workspace_size;
	tData workspace;
	tData kernel;
	int32_t *kernel_size; 



/***************************** 旋转180° *****************************/
#ifdef ROTATE_180_TEST
    out_data = (uint8_t *)malloc(input_size);
    
	// dst.shape_.ndim_ = 3;
    // dst.shape_.dims_[0] = 800;
    // dst.shape_.dims_[1] = 600;
    // dst.shape_.dims_[2] = channel;
    dst.dptr_ = out_data;
	// int32_t *workspace = (int32_t *)malloc(65536);
    ret = rotate(&dst, &src, 1);
	if (ret != 0){
		printf("process failed!\n");
	}
    dump_uint8("rotate_180.txt", out_data, dst.shape_.dims_[0], dst.shape_.dims_[1], dst.shape_.dims_[2], 0, dst.shape_.dims_[2], 1, 'u');
	free(out_data);
#endif
/***************************** 左右翻转 *****************************/
#ifdef FLIP_LEFT_RIGHT_TEST
    out_data = (uint8_t *)malloc(input_size);
    
	// dst.shape_.ndim_ = 3;
    // dst.shape_.dims_[0] = 800;
    // dst.shape_.dims_[1] = 600;
    // dst.shape_.dims_[2] = channel;
    dst.dptr_ = out_data;
	// int32_t *workspace = (int32_t *)malloc(65536);
    ret = rotate(&dst, &src, 4);
	if (ret != 0){
		printf("process failed!\n");
	}
    dump_uint8("flip_left_right.txt", out_data, dst.shape_.dims_[0], dst.shape_.dims_[1], dst.shape_.dims_[2], 0, dst.shape_.dims_[2], 1, 'u');
	free(out_data);
#endif
/***************************** 边缘填充(mode = 0) *****************************/
#ifdef PAD_0_TEST
	int8_t pads[4] = {8,7,10,9};
	uint32_t output_size = (height + pads[0] + pads[2]) * (width + pads[1] + pads[3]) * channel;
    out_data = (uint8_t *)malloc(output_size);
    
	// dst.shape_.ndim_ = 3;
    // dst.shape_.dims_[0] = 800;
    // dst.shape_.dims_[1] = 600;
    // dst.shape_.dims_[2] = channel;
    dst.dptr_ = out_data;
	workspace_size = (int32_t *)malloc((int)pow(10,8));
	
	workspace.shape_.dims_[0] = (int)pow(10,8);
	workspace.dptr_ = workspace_size;
    
	ret = Pad(&dst, &src, pads, 0, 0, &workspace);
	if (ret != 0){
		printf("process failed!\n");
	}
    dump_uint8("pad_0_mode.txt", out_data, dst.shape_.dims_[0], dst.shape_.dims_[1], dst.shape_.dims_[2], 0, dst.shape_.dims_[2], 1, 'u');
	free(out_data);
#endif
/***************************** 最小值滤波 *****************************/
#ifdef MIN_BLUR_TEST
	
    out_data = (uint8_t *)malloc(input_size);
    
	// dst.shape_.ndim_ = 3;
    // dst.shape_.dims_[0] = 800;
    // dst.shape_.dims_[1] = 600;
    // dst.shape_.dims_[2] = channel;
    dst.dptr_ = out_data;
	workspace_size = (int32_t *)malloc((int)pow(10,8));
	
	workspace.shape_.dims_[0] = (int)pow(10,8);
	workspace.dptr_ = workspace_size;
	
	kernel.shape_.dims_[0] = 3;
	kernel.shape_.dims_[1] = 3;
	kernel_size = (int32_t *)malloc(9);
	kernel.dptr_ = kernel_size;
	kernel.scale_ = 0;
    
	ret = filter(&dst, &src, &kernel, 3, &workspace);
	if (ret != 0){
		printf("process failed!\n");
	}
    dump_uint8("minmum_filter.txt", out_data, dst.shape_.dims_[0], dst.shape_.dims_[1], dst.shape_.dims_[2], 0, dst.shape_.dims_[2], 1, 'u');
	free(out_data);
#endif

	// save_bin_file("resize.bin", out_data, 1440000);

	// int32_t err = 0;
	// err = bmp_file_to_image("./opencv/bgr1_cv2.bmp", s_bmpdata, &s_bmp_col, &s_bmp_row);
	// if (err != 0)
	// {
	// 	return -1;
    // }
	// printf("[%s] s_bmp_col = %d, s_bmp_row = %d\n", __func__, s_bmp_col, s_bmp_row);
	// dump_image_to_bmp_file("bgr_test.bmp", s_bmpdata, s_bmp_col, s_bmp_row);
	return ret;
}