ampy --baud 115200 --port /dev/cu.SLAB_USBtoUART put ./../config.json
for file in ../src/*;
do
    ampy --baud 115200 --port /dev/cu.SLAB_USBtoUART put $file
done
picocom /dev/cu.SLAB_USBtoUART -b115200