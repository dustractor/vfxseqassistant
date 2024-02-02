# vfxseqassistant
WIP - midi device script - Will work for other generators besides patcher - VFX Sequencer but the main reason this script exists is I needed a way to copy/paste from program to program.

## Usage:

1. Add a Patcher - VFX Sequencer to the channel rack
2. Right click the VFX Sequencer -> Inputs -> Parameters -> expose the parameters you want to copy.  (This is unimaginably tedious. Right-click,i,p will speed up the process.) Don't expose 9. CurProgram because copy/paste will keep sending you back to the same program.
3. CC# 22 is the message to send to copy. Have the patcher instance selected, not the sequencer, when you send the message.
4. Go to a different program and send CC# 23 to paste the parameters.

If you don't want to go through all that rigamarole, I went ahead and blanked out a VFX Sequencer and saved it as a preset which is included in this repository.

