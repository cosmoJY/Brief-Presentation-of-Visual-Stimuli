% MATLAB R2021a - Psychtoolbox 3.0.17

% Clear the workspace and the screen
sca;
close all;
clearvars;

Screen('Preference','SkipSyncTests', 1);
Screen('Preference','TextRenderer', 0);
rng('shuffle', 'twister');

screenNumber = 0;
whilewhen = 1;
hz = 60;
nrepeat = 10;

if hz == 120
    target_t_lv = [0.008 0.016 0.032 0.048];
elseif hz == 60
    target_t_lv = [0.016 0.032 0.048 0.064];
end
mask_t = 0.016;

% ======================================================
%  스크린 준비: PTB 3
% ======================================================

% Response keys settings
KbName('UnifyKeyNames');
esc = KbName('ESCAPE');
enter = KbName('return'); space = KbName('Space');
upkey = KbName('UpArrow'); downkey = KbName('DownArrow'); rightkey = KbName('RightArrow'); leftkey = KbName('LeftArrow');
qkey = KbName('q'); okey = KbName('o');
key1 = KbName('1!'); key2 = KbName('2@'); key3 = KbName('3#'); key4 = KbName('4$'); key5 = KbName('5%');
key6 = KbName('6^'); key7 = KbName('7&'); key8 = KbName('8*'); key9 = KbName('9('); key0 = KbName('0)');

% color -------------------------------------------------------------------
black = [0 0 0]; white = [255 255 255];

% 윈도우 열기 --------------------------------------------------------
[win, rect]=Screen('OpenWindow', screenNumber, white, [], [], [], [], 0);
SetMouse(rect(3), rect(4));        % 마우스 커서 오른쪽+아래쪽 끝으로 이동

nowtime = fix(clock);
nowdate_txt = sprintf('%4d%02d%02d_%02d%02d%02d', nowtime(1), nowtime(2), nowtime(3), nowtime(4), nowtime(5), nowtime(6));

% ===========================================================================================

imgloc = round(CenterRectOnPointd([0 0 300 400], rect(3)/2, rect(4)/2));
txtloc_y = rect(4)/2-250;

slack = Screen('GetFlipInterval', win)/2;

target = imread('face01.bmp');
mask = imread('mask.bmp');

target_tex = Screen('MakeTexture', win, target);
mask_tex = Screen('MakeTexture', win, mask);
                         
timestamp = [];
for t = 1:nrepeat
    for target_t = target_t_lv
        if whilewhen == 1
            fileName0 = strcat('result/matlab(while)_', num2str(hz), '_', nowdate_txt, '.txt');
            txt = strcat('ptb(while)', num2str(hz), '_' , num2str(target_t*1000), '_', num2str(t));
                                            
            Screen('Flip', win);
            KbPressWait;
            
            target_onset = GetSecs;
            while GetSecs - target_onset < target_t - slack
                DrawFormattedText(win, txt, 'center', txtloc_y, black);
                Screen('DrawTexture', win, target_tex, [], imgloc);
                Screen('Flip', win);
            end

            mask_onset = GetSecs;
            while GetSecs - mask_onset < mask_t - slack
                DrawFormattedText(win, txt, 'center', txtloc_y, black);
                Screen('DrawTexture', win, mask_tex, [], imgloc);
                Screen('Flip', win);
            end
            target_realtime = mask_onset - target_onset;

            mask_offset = GetSecs;
%             while GetSecs - mask_offset < 0.1 - slack
%                 Screen('Flip', win);
%             end
            mask_realtime = mask_offset - mask_onset;

            timestamp = vertcat(timestamp, [t hz whilewhen target_t target_realtime mask_realtime]);
        
        elseif whilewhen == 2
            fileName0 = strcat('result/matlab(when)_', num2str(hz), '_', nowdate_txt, '.txt');
            txt = strcat('ptb(when)', num2str(hz), '_' , num2str(target_t*1000), '_', num2str(t));
            Screen('Flip', win);
            KbPressWait;

            DrawFormattedText(win, txt, 'center', txtloc_y, black);
            Screen('DrawTexture', win, target_tex, [], imgloc);
            target_onset = Screen('Flip',win);  % 사진제시 시작시점

            DrawFormattedText(win, txt, 'center', txtloc_y, black);
            Screen('DrawTexture', win, mask_tex, [], imgloc);
            mask_onset = Screen('Flip', win, target_onset + target_t - slack);    % 사진제시 끝시점 = 차폐 시작시점
            target_realtime = mask_onset - target_onset;

            mask_offset = Screen('Flip', win, mask_onset + mask_t - slack);     % 차폐제시 끝시점 = 빈화면 제시시점
            mask_realtime = mask_offset - mask_onset;

%             Screen('Flip', win, mask_offset + 0.1 - slack);
            timestamp = vertcat(timestamp, [t hz whilewhen target_t target_realtime mask_realtime]);
        end
    end
end

writetable(table(timestamp), fileName0, 'Delimiter', '\t');
Screen('Close', win);