# PsychoPy 2022.1.3 & Python 3.6
# Monitor test: Temporal resolution

from psychopy import visual, core, event, data, gui, logging, monitors, tools, parallel #import some libraries from PsychoPy
from psychopy.hardware import keyboard
from psychopy.tools import colorspacetools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray, arctan
from numpy.random import random, randint, normal, shuffle
import random
import os #handy system and path functions
import glob # Filename globbing utility.
from PIL import Image # Get the size(demension) of an images

# =====================================================================================================
 
nrepeat = 10
hz = 60
slack = 1/hz/2
whilewhen = 2

frameTolerance = 0.001  # how close to onset before 'same' frame

waitClock = core.Clock()
key_resp = keyboard.Keyboard(backend='ptb')
ptargetClock = core.Clock()
pmaskClock = core.Clock()
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

location = 2
if hz == 60:
    target_t_lv = [0.016, 0.032, 0.048, 0.064]; 
elif hz == 120:
    target_t_lv = [0.008, 0.016, 0.032, 0.048]; 
mask_t = 0.016;


screenNumber = 0;         # 모니터 스크린 번호

#----------------------------------------------
# Sttings: Stim. Size & Location etc.
#----------------------------------------------

monitor_inch = 24; distance_cm = 70; monitorX = 1920; monitorY = 1080;

bgColorRGB = [255,255,255]

# create a window
win = visual.Window([monitorX, monitorY], screen = screenNumber, fullscr = 'bool', units='pix', color = bgColorRGB, colorSpace = 'rgb255', multiSample = False)   # anti-aliasing (multiSample = True, numSamples = 16)  # fullscr = 'bool',
win.mouseVisible = False

centerx = 0; centery = 0

#----------------------------------------------
# Exp. start
#----------------------------------------------

target = visual.ImageStim(win, image = "face01.bmp", size = (300, 400), pos = (centerx, centery), units = "pix")
mask = visual.ImageStim(win, image = "mask.bmp", size = (300, 400), pos = (centerx, centery), units = "pix")
txtloc_y = centery + 250

timestamp = np.empty((0, 6), int)
for t in range(0, nrepeat):
    tcurrent = t
    for target_t in target_t_lv:
        
        if whilewhen == 1:
            text = visual.TextStim(win, text= 'psychopy(while)' +  str(hz) + '_' + str(target_t*1000) + '_' + str(t), pos = (centerx, txtloc_y), units = 'pix', height = 30, color = 'black', bold = False)
            
            win.flip()
            kb = keyboard.Keyboard(backend='ptb')
            kb.waitKeys(waitRelease=False)
            
            clock = core.Clock()
            while clock.getTime() < target_t - slack:
                target.draw(); text.draw()
                win.flip()
            target_realtime = clock.getTime()
        
            clock_m = core.Clock() 
            while clock_m.getTime() < mask_t - slack:
                mask.draw(); text.draw()
                win.flip()
            mask_realtime = clock_m.getTime()
        if whilewhen == 2:
            text = visual.TextStim(win, text= 'psychopy(when)' +  str(hz) + '_' + str(target_t*1000) + '_' + str(tcurrent), pos = (centerx, txtloc_y), units = 'pix', height = 30, color = 'black', bold = False)
            
#            win.flip()
#            kb = keyboard.Keyboard(backend='ptb')
#            kb.waitKeys(waitRelease=False)

            # ------Prepare to start Routine "wait"-------
            continueRoutine = True
            # update component parameters for each repeat
            key_resp.keys = []
            key_resp.rt = []
            _key_resp_allKeys = []
            # keep track of which components have finished
            waitComponents = [key_resp]
            for thisComponent in waitComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            ttime = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            waitClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            # -------Run Routine "wait"-------
            while continueRoutine:
                # get current time
                t = waitClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=waitClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # *key_resp* updates
                waitOnFlip = False
                if key_resp.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    key_resp.frameNStart = frameN  # exact frame index
                    key_resp.tStart = ttime  # local t and not account for scr refresh
                    key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                    key_resp.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if key_resp.status == STARTED and not waitOnFlip:
                    theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
                    _key_resp_allKeys.extend(theseKeys)
                    if len(_key_resp_allKeys):
                        key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                        key_resp.rt = _key_resp_allKeys[-1].rt
                        # a response ends the routine
                        continueRoutine = False
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in waitComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            # -------Ending Routine "wait"-------
            for thisComponent in waitComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "wait" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()

            # ------Prepare to start Routine "ptarget"-------
            continueRoutine = True
            # update component parameters for each repeat
                # keep track of which components have finished
            ptargetComponents = [target, text]
            for thisComponent in ptargetComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            ttime = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            ptargetClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            # -------Run Routine "ptarget"-------
            while continueRoutine:
                # get current time
                ttime = ptargetClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=ptargetClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *target* updates
                if target.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    target.frameNStart = frameN  # exact frame index
                    target.tStart = ttime  # local t and not account for scr refresh
                    target.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(target, 'tStartRefresh')  # time at next scr refresh
                    target.setAutoDraw(True)
                if target.status == STARTED:
                    if tThisFlipGlobal > target.tStartRefresh + target_t-frameTolerance:
                        # keep track of stop time/frame for later
                        target.tStop = ttime  # not accounting for scr refresh
                        target.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(target, 'tStopRefresh')  # time at next scr refresh
                        target.setAutoDraw(False) 
                         
                # *text* updates
                if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text.frameNStart = frameN  # exact frame index
                    text.tStart = ttime  # local t and not account for scr refresh
                    text.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
                    text.setAutoDraw(True)
                if text.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > text.tStartRefresh + target_t-frameTolerance:
                        # keep track of stop time/frame for later
                        text.tStop = ttime  # not accounting for scr refresh
                        text.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(text, 'tStopRefresh')  # time at next scr refresh
                        text.setAutoDraw(False)
                        
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in ptargetComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            # -------Ending Routine "ptarget"-------
            
            for thisComponent in ptargetComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            target_realtime = tThisFlipGlobal - target.tStartRefresh # ptargetClock.getTime()
            # the Routine "ptarget" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "pmask"-------
            continueRoutine = True
            routineTimer.add(mask_t)
            text_2 = text
            # keep track of which components have finished
            pmaskComponents = [mask, text_2]
            for thisComponent in pmaskComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            ttime = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            pmaskClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            # -------Run Routine "pmask"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                ttime = pmaskClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=pmaskClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # *mask* updates
                if mask.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    mask.frameNStart = frameN  # exact frame index
                    mask.tStart = ttime  # local t and not account for scr refresh
                    mask.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mask, 'tStartRefresh')  # time at next scr refresh
                    mask.setAutoDraw(True)
                if mask.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > mask.tStartRefresh + mask_t-frameTolerance:
                        # keep track of stop time/frame for later
                        mask.tStop = ttime  # not accounting for scr refresh
                        mask.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(mask, 'tStopRefresh')  # time at next scr refresh
                        mask.setAutoDraw(False)
                # *text_2* updates
                if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text_2.frameNStart = frameN  # exact frame index
                    text_2.tStart = ttime  # local t and not account for scr refresh
                    text_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
                    text_2.setAutoDraw(True)
                if text_2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > text_2.tStartRefresh + mask_t-frameTolerance:
                        # keep track of stop time/frame for later
                        text_2.tStop = ttime  # not accounting for scr refresh
                        text_2.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(text_2, 'tStopRefresh')  # time at next scr refresh
                        text_2.setAutoDraw(False)
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in pmaskComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            # -------Ending Routine "pmask"-------
            for thisComponent in pmaskComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            mask_realtime = tThisFlipGlobal - mask.tStartRefresh  #pmaskClock.getTime()
        timestamp  = np.append(timestamp, np.array([[tcurrent, hz, whilewhen, target_t, target_realtime, mask_realtime]]), axis = 0);  # 행 추가

dataFileName='result' + os.path.sep + 'PsychoPy(while)_' + str(hz) + '_' + data.getDateStr() + '.txt'
np.savetxt(dataFileName, timestamp, delimiter='\t', fmt='%f')

#kb = keyboard.Keyboard()
#while True:
#    keys = kb.getKeys(['escape', 'space', 'z', 'slash'])  
#    if 'escape' in keys:
#        core.quit()
#
