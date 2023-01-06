#ifndef _GET_ZHUANGJIABAN_CPP
#define _GET_ZHUANGJIABAN_CPP

#include<iostream>
#include<vector>
#include<cmath>
#include<conio.h>
#include<opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

const int kThreashold = 100;
const int kMaxVal = 255;
enum CLOR{blue=0,red=1};
const double Pi = 3.1415926535897932;
const Size kGaussianBlueSize = Size(5, 5);

enum ArmorType {
	BIG_ARMOR = 0,
	SMALL_ARMOR = 1,//由于我们没造出大装甲板，只有小装甲板
	NO_ARMOR = 2
};
struct ArmorCorners {
	Point2f rt; // Right-Top
	Point2f lt; // Left-Top
	Point2f ld; // Left-Down
	Point2f rd; // Right-Down
};
struct ArmorPredResult {
	ArmorCorners corners_cam_coord;
	float confidence; // 0 to 1
	ArmorType armor_type;
};
inline Mat Minus(Mat image, int mode, int grayThres){
	Mat grayImg = image.clone();
    Mat channels[3];
	split(image, channels);
	if (mode) {
		grayImg = channels[2] -channels[0];
	}
	else {
		grayImg = channels[0]- channels[2];
	}
	return grayImg;
}
//获取二值化图像
inline Mat GrayFilter(Mat image, int mode, int grayThres) { //grayThres可视为kThreashold，识别red是1，否则为0
	Mat grayImg = Minus(image,mode,grayThres).clone();
	threshold(grayImg, grayImg, 0, 255, THRESH_OTSU);
	//threshold(grayImg, grayImg, kThreashold, 255, THRESH_BINARY);
	//adaptiveThreshold(grayImg, grayImg, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY,9,10);
	return grayImg;
}
//struct fpoints
inline Mat enhanceContour(Mat image) { //腐蚀膨胀
	int niters = 2;
	Mat copied_image = image.clone();
	Mat kernel = getStructuringElement(2, Size(3, 3), Point2f(-1, -1)); // 0为MORPH_RECT

	erode(copied_image, copied_image, kernel, Point2f(-1, -1), niters);
		//morphologyEx(copied_image, copied_image,3, kernel, Point2f(-1, -1),MORPH_OPEN); //
	dilate(copied_image, copied_image, kernel, Point2f(-1, -1), niters);
	return copied_image;
}
inline double arcle(Rect x, Rect y) {
	double h_l = x.x + 0.5 * x.width - y.x - 0.5 * y.width;
	double y_l = y.y - x.y;
	double y_2 = x.y + x.height - y.height - y.y;
	return max(abs(y_l / h_l), abs(y_2 / h_l));
}
inline double arearate(Rect x, Rect y) {
	double h_1 = 0.5 * x.height + 0.5 * y.height;
	double y_1 = abs(x.width * 0.5 + x.x - 0.5 * y.width - y.x);
	return y_1 / h_1;

}
inline double deltarate(Rect x, Rect y) {
	double yy = x.height * 0.5 + x.y - 0.5 * y.height - y.y;
	double xx = x.width * 0.5 + x.x - 0.5 * y.width - y.x;
	return abs(yy / xx);
}
inline double shaperate(Rect x, Rect y) {
	double yy = (1.0 * y.height) / (1.0 * x.height);
	double xx = (y.width) / (1.0 * x.width);
	return abs(max(yy, xx) / min(yy, xx));
}
vector<ArmorPredResult> detect(Mat img,CLOR clour) {
	cout << "new_data" << endl;
	vector<ArmorPredResult> my_detect;
	ArmorPredResult my;
	my.confidence = 1.0;
	my.armor_type = NO_ARMOR;

	Mat frame, Gaussian;
	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;
	Rect boundRect;
	RotatedRect box;
	vector<Point2f> boxPts(4);
	//for (;;) {
	vector<Rect>point_array;
	frame = img.clone();
	// cout << "1" << endl;
	//frame = imread("C:/Users/Administrator/Desktop/d88d449b491b4a96b16279b78134c317.png");
	if (frame.empty()) {
		cout << "detect:frame is empty" << endl;
		return my_detect;
		//break;
	}
	Mat binary = GrayFilter(frame, clour, kThreashold).clone();
	Mat gray;
	
	// GaussianBlur(binary, Gaussian,kGaussianBlueSize, 0);
	gray=Minus(img,clour,24).clone();
	//cvtColor(gray,gray,COLOR_BGR2GRAY);
	Gaussian = enhanceContour(binary).clone();
	findContours(Gaussian, contours, hierarchy, RETR_TREE, CHAIN_APPROX_NONE);
	Mat grayy = Mat::zeros(Gaussian.rows, Gaussian.cols, CV_8UC3);
	
	int index = 0;
	for (int i = 0; i < contours.size(); i++) {
		//box = minAreaRect(Mat(contours[i]));
		//box.points(boxPts.data());


		boundRect = boundingRect(Mat(contours[i]));
		//rectangle(frame, boundRect.tl(), boundRect.br(), (0, 255, 0), 2,8 ,0);

		try {
			double bili = (1.0 * boundRect.height / (1.0 * boundRect.width));
			if (bili >= 1.6) {
				point_array.push_back(boundRect);
				index++;
				Scalar color(238, 128, 234);
				drawContours(grayy, contours, i, color, FILLED, 8);
				//	 drawContours(gray, contours,i,color,FILLED,8);
				//	 cout << "we get it" << endl;

			}
			//cout << "bili=" << bili << endl;
		}
		catch (const char* msg) {
			cout << printf(msg) << endl;
			//continue;
		}
	}


	int point_near[2];
	double minm = 1000000;
	bool ppt = false;
	for (int i = 0; i < index - 1; i++) {
		for (int j = i + 1; j < index; j++) {
			//int count_area=abs(point_array[i].x+point_array[i].width/2-point_array[j].x - point_array[j].width / 2 )*abs(point_array[i].height/2+point_array[j].height/2);
			int value = abs(point_array[i].area() - point_array[j].area());
			//cout << "1area=" << point_array[i].area() << ",2area=" << point_array[j].area() << endl;
			//float value = point_array[i].area()/point_array[j].area();
		//	if (arearate(point_array[i], point_array[j]) <= 2.2 && deltarate(point_array[i], point_array[j]) <=0.2) 
			cout << "delta_rate=" << deltarate(point_array[i], point_array[j]) << endl;
				cout << "shape_rate="<< shaperate(point_array[i], point_array[j]) <<endl;
				cout << "area_rate="<< arearate(point_array[i], point_array[j] )<<endl;
				cout << "arcle=" << arcle(point_array[i], point_array[j]) <<endl;
				//cout<<endl;
			if (
				arcle(point_array[i], point_array[j]) <= 0.5
				&& shaperate(point_array[i], point_array[j]) <= 1.64
				&& shaperate(point_array[i], point_array[j]) >= 0.7
				&& arearate(point_array[i], point_array[j]) <= 2.54
				&& arearate(point_array[i], point_array[j]) >= 1
				)
			{
				cout << "we get it" << endl<<endl;
				my.armor_type = SMALL_ARMOR;
				ppt = true;
				minm = value;
				point_near[0] = i;
				point_near[1] = j;
				//绘制框
				try {
					//cout << "pr=" << point_near[0] << endl;
					Rect rectangle_1 = point_array[point_near[0]];
					Rect rectangle_2 = point_array[point_near[1]];
					if (rectangle_2.x == 0 || rectangle_1.x == 0) {
						throw "not enough points";
					}
					Point2f point1 = Point2f(rectangle_1.x + rectangle_1.width / 2.0, rectangle_1.y);
					Point2f point2 = Point2f(rectangle_1.x + rectangle_1.width / 2.0, rectangle_1.y + rectangle_1.height);
					Point2f point3 = Point2f(rectangle_2.x + rectangle_2.width / 2.0, rectangle_2.y);
					Point2f point4 = Point2f(rectangle_2.x + rectangle_2.width / 2.0, rectangle_2.y + rectangle_2.height);
					Point2f p[4] = { point1,point2,point4,point3 };
					if (p[0].x > p[2].x) {
						Point2f t = p[0];
						p[0] = p[2];
						p[2] = t;
						t = p[1];
						p[1] = p[3];
						p[3] = t;
					}
					my.corners_cam_coord.rd = p[3];
					my.corners_cam_coord.rt = p[2];
					my.corners_cam_coord.lt = p[1];
					my.corners_cam_coord.ld = p[0];
					my_detect.push_back(my);
					my.armor_type = NO_ARMOR;
					my.confidence = 1.0;
					//cout << p[0] << p[1] << p[2] << p[3] << endl;
					for (int k = 0; k < 4; k++) {
						line(frame, p[k % 4], p[(k + 1) % 4], Scalar(0, 255, 0), 2);
					}
				}

				catch (const char* msg) {
					cout << msg << endl;
					//continue;
				}
			}else{
				cout<<"not this"<<endl<<endl;
			}
		}
	}
	resize(gray, gray, Size(640, 640));
	resize(grayy, grayy, Size(640, 640));
	resize(frame, frame, Size(640, 640));
	imshow("grayy", grayy);
	imshow("video", frame);
	imshow("gray", gray);
	//destroyAllWindows();
	/*if (waitKey(30) >= 0) {
	   break;
	}*/
	//  }
	/* video.release();
	 cv::destroyAllWindows();*/

	return my_detect;
}

#endif