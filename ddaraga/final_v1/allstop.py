from gpio import IO
from detec_tag import Tag

tag =Tag()
io = IO()

tag.robot.allstop()
tag.robot.init()
io.clean()