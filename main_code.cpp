#include"get_zhuangjiaban.h"
int main() {
	VideoCapture video;
	video.open("C:\\Users\\Administrator\\Desktop\\data\\b786b4f05b7afe05730742fed4b8aa92(1).mp4");
	for (;;) {
		Mat img;
		video >> img;
		CLOR clour=blue;
		//img = imread("C:/Users/Administrator/Desktop/QQ图片20221122230157.png");
		vector<ArmorPredResult> me = detect(img,clour);
		ArmorPredResult my;
		for (int i = 0; i < me.size(); i++)
		{
			my = me[i];
			if (my.armor_type == NO_ARMOR)
			{
				continue;
			}
			else
			{

				cout << my.corners_cam_coord.ld << " and " << my.corners_cam_coord.rd << " and " << my.corners_cam_coord.lt << " and " << my.corners_cam_coord.rt << endl;
			}
		}
		waitKey(0);
		cout<<endl<<endl;
		//system("pause");
	}
	return 0;
}