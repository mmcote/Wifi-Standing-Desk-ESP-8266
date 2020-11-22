echo ">>> Loading config.json"
ampy --baud 115200 --port /dev/cu.SLAB_USBtoUART put ./../config.json
for file in ../src/*;
do
    echo ">>> Loading ${file}"
    ampy --baud 115200 --port /dev/cu.SLAB_USBtoUART put $file
done

# Reset the board
echo ">>> Resetting the board"
ampy --baud 115200 --port /dev/cu.SLAB_USBtoUART reset

picocom /dev/cu.SLAB_USBtoUART -b115200