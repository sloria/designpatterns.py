"""Command pattern.

- Decouples an object making a request (invoker) from the object doing the work
    to perform the request (receiver).
- Allows parameterization of different requests and support undoable operations
"""

# Receivers may have different interfaces
class Light:

    def __init__(self, room):
        self.room = room
        self.active = False

    def on(self):
        self.active = True

    def off(self):
        self.active = False

class Stereo:
    def __init__(self, cd=None):
        self.cd = cd
        self.volume = 0
        self.playing = False

    def play_cd(self):
        self.playing = True

    def stop_cd(self):
        self.playing = False

# The commands have a unified interface

class LightOnCommand:

    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()

class LightOffCommand:

    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.off()

    def undo(self):
        self.light.on()

class StereoOnWithCDCommand:
    def __init__(self, stereo):
        self.stereo = stereo
        self.prev_volume = None

    def execute(self):
        self.prev_volume = self.stereo.volume  # Save previous volume
        self.stereo.play_cd()
        self.stereo.volume = 11

    def undo(self):
        self.stereo.stop_cd()
        self.stereo.volume = self.prev_volume

class StereoOffCommand:
    def __init__(self, stereo):
        self.stereo = stereo

    def execute(self):
        self.stereo.stop_cd()

    def undo(self):
        self.stereo.play_cd()

class NoCommand:  # Null object, so remote doesn't have to handle AttributeError
    def execute(self):
        return None

    def undo(self):
        return None

class RemoteControl:
    """A remote control for home automation with 7 programmable slots,
    each with an on and off button.
    Also has a global undo button that undoes the last button pressed.
    """
    def __init__(self):
        # Store slots as two arrays
        no_command = NoCommand()
        self.on_commands = [no_command for _ in range(7)]
        self.off_commands = [no_command for _ in range(7)]
        self.undo_command = no_command

    def set_command(self, slot, on_command, off_command):
        self.on_commands[slot] = on_command
        self.off_commands[slot] = off_command

    def on_pushed(self, slot):
        command = self.on_commands[slot]
        command.execute()
        self.undo_command = command


    def off_pushed(self, slot):
        command = self.off_commands[slot]
        command.execute()
        self.undo_command = command

    def undo_pushed(self):
        self.undo_command.undo()

    def __str__(self):
        # prints the content of each slot
        return '\n'.join(["Slot {}:\t{}\t{}".format(i, on_cmd.__class__, off_cmd.__class__)
            for i, (on_cmd, off_cmd) in
            enumerate(zip(self.on_commands, self.off_commands))])


def test_remote():
    rc = RemoteControl()
    light = Light("Living Room")
    stereo = Stereo()
    rc.set_command(0, LightOnCommand(light), LightOffCommand(light))
    rc.set_command(1, StereoOnWithCDCommand(stereo), StereoOffCommand(stereo))
    rc.on_pushed(1)
    assert stereo.playing is True
    assert stereo.volume == 11
    rc.on_pushed(0)
    assert light.active is True
    rc.off_pushed(1)
    assert stereo.playing is False
    rc.on_pushed(2)
    assert stereo.playing is False

def test_undo():
    rc = RemoteControl()
    light = Light("Living Room")

    light_on_cmd = LightOnCommand(light)
    light_off_cmd = LightOffCommand(light)

    rc.set_command(0, light_on_cmd, light_off_cmd)
    rc.on_pushed(0)
    assert light.active is True
    rc.undo_pushed()
    assert light.active is False
