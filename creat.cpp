#include <opencv2/opencv.hpp>
#include<iostream>
#define CV_COLOR_RED cv::Scalar(48, 180, 80)
using namespace std;
using namespace cv;
int main(int argc, char** argv)
{
	CascadeClassifier faceDetector("D:\\zanghaomin\\mydata\\20221202xml\\cascade.xml");
	Mat grayy;
	VideoCapture vedio;
	vedio.open("D:\\zanghaomin\\yolov5-master\\data\\vedio\\k.mp4");
	Mat image;
//image = imread("C:\\Users\\Administrator\\Desktop\\data\\0002.jpg",1);
  while(1)  
    {
	vedio>>image;
		resize(image,grayy,Size(640,640));
	//copyMakeBorder(image,grayy,0,640,0,640,0);
	vector<Rect> objects;
	faceDetector.detectMultiScale(grayy, objects);
    int niters;
	if(objects.size()>3) niters=3;
	else niters=objects.size();
	for (int i = 0; i <objects.size(); i++)
	{
		rectangle(grayy, objects[i], CV_COLOR_RED);
	}
	
	imshow("result", grayy);
	waitKey(40);
	}
	return 0;
}