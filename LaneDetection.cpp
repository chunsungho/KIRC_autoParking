#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <stdio.h>

using namespace cv;
using namespace std;

#define FILTER_SIZE 5

Mat img_bgr, img_hsv, img_binary, img_gray, img_edge, img_contours, img_roi, img_hough, img_line, img_annotated, img_result;
Point2f leftP[2], rightP[2], vanishP;
Point p0 = Point(0, 0);

//hsv Ʈ���ٿ��� ���Ǵ� ���� 
int LowH = 0; //0;//0
int HighH = 144; //52;//17
int LowS = 118; //0;//150
int HighS = 255; //67;//255
int LowV = 118; //88
int HighV = 255; //255
				 //Canny edge Ʈ���� ����
int lowThreshold = 50;
int highThreshold = 150;

double g_Sum_x;
double g_Buf_x[FILTER_SIZE];
int g_Cnt_x;
double g_Filtered_x;

double g_Sum_y;
double g_Buf_y[FILTER_SIZE];
int g_Cnt_y;
double g_Filtered_y;

double movingAFilter_x(int input) {

	//int sum = 0 ;
	g_Sum_x -= g_Buf_x[g_Cnt_x];
	g_Buf_x[g_Cnt_x++] = input;
	g_Sum_x += input;

	if (g_Cnt_x == FILTER_SIZE) g_Cnt_x = 0;

	return (double)(g_Sum_x) / FILTER_SIZE;

}

double movingAFilter_y(int input) {

	//int sum = 0 ;
	g_Sum_y -= g_Buf_y[g_Cnt_y];
	g_Buf_y[g_Cnt_y++] = input;
	g_Sum_y += input;

	if (g_Cnt_y == FILTER_SIZE) g_Cnt_y = 0;

	return (double)(g_Sum_y) / FILTER_SIZE;
}


void filter_color()
{	//Ư������ �����ϴ� �Լ�
	cvtColor(img_bgr, img_hsv, COLOR_BGR2HSV); //hsv�������� ��ȯ
	inRange(img_hsv, Scalar(LowH, LowS, LowV), Scalar(HighH, HighS, HighV), img_binary); //Ư���� ����

																						 //morphological opening ���� ������ ���� 
	erode(img_binary, img_binary, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
	dilate(img_binary, img_binary, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));

	//morphological closing ������ ���� �޿�� 
	dilate(img_binary, img_binary, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
	erode(img_binary, img_binary, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
}

void line_detect(Mat &img_line, vector<Vec2f> lines)
{	//��ǥ���� �����ϴ� �Լ�

	img_line = img_bgr.clone();

	vector<Vec2f> right_lines;
	vector<Vec2f> left_lines;

	for (size_t i = 0; i < lines.size(); i++)
	{
		Vec2f l = lines[i];		// ���⿡ ���� ������ ����Ǵ°���?

		double rho = l[0];
		double theta = l[1];

		if (theta < CV_PI * 2 / 5)	//72��
		{
			right_lines.push_back(l);	//����ȣ �ҽ�
			//left_lines.push_back(l); //���� ���� ����
		}
		else if (theta > CV_PI * 3 / 5)	//108��		-> ��¶�� ���߿� �ٲ�� �ϴ� ��ġ. ���� : ī�޶��� ��ġ�� ���� ���� ������ �ٸ��Ժ���
		{
			left_lines.push_back(l); //����ȣ �ҽ�
			//right_lines.push_back(l); //������ ���� ����
		}

		float resultLine[2][2];

		for (int i = 0; i < left_lines.size(); i++)
		{
			// Theta�� ���� ū �� 1���� ����
			resultLine[0][0] = left_lines[0][0];
			resultLine[0][1] = left_lines[0][1];

			for (size_t i = 1; i < left_lines.size(); i++)
			{
				if (left_lines[i][1] >= resultLine[0][1])	//�ٲ�
				{
					resultLine[0][0] = left_lines[i][0];
					resultLine[0][1] = left_lines[i][1];
				}
			}

			double rho = resultLine[0][0];
			double theta = resultLine[0][1];

			//���׸��� �ҷ��� ��ǥ�� ����ؾ���
			double a = cos(theta), b = sin(theta);
			double x0 = a * rho, y0 = b * rho;
			double x1 = (cvRound(x0 + (img_edge.rows + img_edge.cols) * (-b)));
			double y1 = (cvRound(y0 + (img_edge.rows + img_edge.cols) * (a)));// +img_edge.rows / 2);
			double x2 = (cvRound(x0 - (img_edge.rows + img_edge.cols) * (-b)));
			double y2 = (cvRound(y0 - (img_edge.rows + img_edge.cols) * (a)));// +img_edge.rows / 2);

			leftP[0].x = x1;
			leftP[0].y = y1;
			leftP[1].x = x2;
			leftP[1].y = y2;

			line(img_line, Point(x1, y1), Point(x2, y2), Scalar(255, 255, 0), 4, CV_8UC3); //���� ���� �׸���
		}

		for (int i = 0; i < right_lines.size(); i++)
		{
			// Theta�� ���� ���� �� 1���� ����
			resultLine[1][0] = right_lines[0][0];
			resultLine[1][1] = right_lines[0][1];

			for (size_t i = 1; i < right_lines.size(); i++)
			{
				if (right_lines[i][1] < resultLine[1][1])
				{
					resultLine[1][0] = right_lines[i][0];
					resultLine[1][1] = right_lines[i][1];
				}
			}
			double rho = resultLine[1][0];
			double theta = resultLine[1][1];

			//���׸��� �ҷ��� ��ǥ�� ����ؾ���
			double a = cos(theta), b = sin(theta);
			double x0 = a * rho, y0 = b * rho;
			double x1 = (cvRound(x0 + (img_edge.rows + img_edge.cols) * (-b)));
			double y1 = (cvRound(y0 + (img_edge.rows + img_edge.cols) * (a)));// +img_edge.rows / 2);
			double x2 = (cvRound(x0 - (img_edge.rows + img_edge.cols) * (-b)));
			double y2 = (cvRound(y0 - (img_edge.rows + img_edge.cols) * (a)));// +img_edge.rows / 2);

			rightP[0].x = x1;
			rightP[0].y = y1;
			rightP[1].x = x2;
			rightP[1].y = y2;

			line(img_line, Point(x1, y1), Point(x2, y2), Scalar(255, 0, 255), 4, CV_8UC3); //������ ���� �׸���
		}
	}
}

int main()
{
	VideoCapture videoCapture("yellow_test3.mp4"); //�����νĵ����� �ҷ�����
												   //VideoCapture videoCapture(0); //��ķ �ҷ�����

	if (!videoCapture.isOpened())
	{
		cout << "�������� ���� �����ϴ�. \n" << endl;

		char a;
		cin >> a;

		return -1;
	}

	/*// hsv Ʈ����
	namedWindow("Ư���� ����", WINDOW_AUTOSIZE);
	createTrackbar("LowH", "Ư���� ����", &LowH, 179); //Hue (0 - 179)
	createTrackbar("HighH", "Ư���� ����", &HighH, 179);
	createTrackbar("LowS", "Ư���� ����", &LowS, 255); //Saturation (0 - 255)
	createTrackbar("HighS", "Ư���� ����", &HighS, 255);
	createTrackbar("LowV", "Ư���� ����", &LowV, 255); //Value (0 - 255)
	createTrackbar("HighV", "Ư���� ����", &HighV, 255);*/

	while (1)
	{
		videoCapture.read(img_bgr); //�������� �ҷ���
		if (img_bgr.empty()) break;

		filter_color(); //Ư���� ����
						//cvtColor(img_bgr, img_gray, COLOR_BGR2GRAY); //���� ������� ��ȯ
		GaussianBlur(img_binary, img_binary, Size(5, 5), 0, 0); //����þ� ��(Size�� ������ ����,���ڰ� Ŭ���� ������)
		Canny(img_binary, img_edge, lowThreshold, highThreshold); //ĳ�Ͽ��� ����

		//�ٷ� ������ ���´�
		Mat img_roi(img_edge, Rect(0, 0, img_edge.cols, img_edge.rows)); //�̹��� ���ɿ��� ����

		vector<Vec2f> lines;
		HoughLines(img_roi, lines, 1, CV_PI / 180, 100, 0, 0, 0, CV_PI);
		line_detect(img_line, lines); //���� ����


		 //�ҽ��� ����
		float leftLineA = (float)(leftP[1].y - leftP[0].y) / (float)(leftP[1].x - leftP[0].x);
		float leftLineB = leftP[1].y - leftLineA * leftP[1].x;
		float rightLineA = (float)(rightP[1].y - rightP[0].y) / (float)(rightP[1].x - rightP[0].x);
		float rightLineB = rightP[1].y - rightLineA * rightP[1].x;

		// 1�� �ҽ���: �¿� 1������ ����
		vanishP.x = (double)((rightLineB - leftLineB) / (leftLineA - rightLineA));
		vanishP.y = (double)(leftLineA * vanishP.x + leftLineB);

		vanishP.x = movingAFilter_x(vanishP.x);
		vanishP.y = movingAFilter_y(vanishP.y);

		double slope;
		if (vanishP.x - img_line.cols * 0.5 == 0)
			slope = 999.00; // ����
		else
		{
			if (vanishP.y < 0)
				slope = (float)(img_line.rows - vanishP.y) / (float)(vanishP.x - img_line.cols * 0.5);
			else
				slope = (float)(img_line.rows - vanishP.y) / (float)(vanishP.x - img_line.cols * 0.5);


		}
		printf("���� : %f\n", slope);

		// ���⼭ line �Լ� ���ֱ����� vanishP ��� ���� �̵���� ���͸� ���� �� ������ ���־�� �Ѵ�.
		line(img_line, Point(img_line.cols * 0.5, img_line.rows), vanishP, Scalar(0, 255, 0), 4, CV_8UC3);

		//hconcat(img_line, img_roi, img_result); //���� ���η� ���̱�
		//imshow("���� ����", img_bgr);
		//imshow("����ȭ ����", img_binary);
		//imshow("���� ����", img_edge);
		imshow("��������", img_line);
		imshow("���ɿ���", img_roi);


		if (waitKey(1) == 27) break; //ESCŰ ������ ���� 
		/*
		leftP[0] = Point(0,0);
		leftP[1] = Point(0, 0);
		rightP[0] = Point(0, 0);
		rightP[1] = Point(0, 0);*/

	}

	return 0;

}