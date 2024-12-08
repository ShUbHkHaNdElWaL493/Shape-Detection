/*
    Shubh Khandelwal
*/

#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>
#include <opencv2/opencv.hpp>
#include <ros/ros.h>
#include <sensor_msgs/Image.h>

int main(int argc, char** argv)
{

    ros::init(argc, argv, "camera_publisher");
    ros::NodeHandle nh;

    image_transport::ImageTransport image_transport(nh);
    image_transport::Publisher image_publisher = image_transport.advertise("/feed", 1);
    cv::Mat frame;
    sensor_msgs::ImagePtr msg;

    cv::VideoCapture camera(2);
    if (!camera.isOpened())
    {
        ROS_ERROR("Could not open video stream");
        return -1;
    }
    camera.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    camera.set(cv::CAP_PROP_FRAME_HEIGHT, 360);

    ros::Rate loop_rate(90);

    while (ros::ok())
    {
    
        camera>>frame;
        if (frame.empty())
        {
            ROS_WARN("Captured empty frame");
            break;
        }
    
        msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", frame).toImageMsg();
        image_publisher.publish(msg);
    
        ros::spinOnce();
        loop_rate.sleep();
    
    }

    return 0;

}
