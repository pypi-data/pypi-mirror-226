# coding=utf-8
from pymycobot import MyArm
from pymycobot.common import ProtocolCode, write, read


class CobotX(MyArm):
    def __init__(self, port, baudrate="115200", timeout=0.1, debug=False):
        super().__init__(port, baudrate, timeout, debug)
        
    def set_solution_angles(self, angle, speed):
        """Set zero space deflection angle value
        
        Args:
            angle: Angle of joint 1.
            speed: 1 - 100.
        """
        return self._mesg(ProtocolCode.COBOTX_SET_SOLUTION_ANGLES, [self._angle2int(angle)], speed)
    
    def get_solution_angles(self):
        """Get zero space deflection angle value"""
        return self._mesg(ProtocolCode.COBOTX_GET_SOLUTION_ANGLES, has_reply=True)
    
    def write_move_c(self, transpoint, endpoint, speed):
        """_summary_

        Args:
            transpoint (_type_): _description_
            endpoint (_type_): _description_
            speed (_type_): _description_
        """
        start = []
        end = []
        for index in range(6):
            if index < 3:
                start.append(self._coord2int(transpoint[index]))
                end.append(self._coord2int(endpoint[index]))
            else:
                start.append(self._angle2int(transpoint[index]))
                end.append(self._angle2int(endpoint[index]))
        return self._mesg(ProtocolCode.WRITE_MOVE_C, start, end, speed)