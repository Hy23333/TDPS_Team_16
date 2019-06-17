import cv2
import xf_color
import serial
ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
def videox():
    vix = cv2.VideoCapture(0)
    while True:
        ret, tu = vix.read()
        cv2.imshow("take_photo", tu)
        cv2.waitKey(1)
        cv2.imwrite("color.png", tu)
        filename = cv2.imread("color.png")
        color = xf_color.get_color(filename)

        if  color == "blue":
            print("blue")
            result = "1"
            break
        elif color == "red" or color == "red2":
            print("red")
            result = "2"
            break
        elif color == "green":
            print("green")
            result = "3"
            break
        elif color == "white":
            print("white")
            result = "4"
            break
    ser.write(result.encode())
    vix.release()
    cv2.destroyAllWindows()
    return result


if __name__ == '__main__':
    videox()