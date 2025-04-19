xhost local:root

XAUTH=/tmp/.docker.XAUTH

docker run -it \
    --name=linux_gui_r1 \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --net=host \
    --privileged \
    --runtime=nvidia \
    osrf/ros:noetic-desktop-full
    bash \

echo "Done."
