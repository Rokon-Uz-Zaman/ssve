import sys
import os
import datetime

def parse_source_line(line, sources):
    split = line.find(' ')
    name = line[:split]
    video = line[split + 1:]
    sources[name] = video

def parse_clip_line(line, clips):
    name, source, start, end = line.split(' ')
    clips[name] = {'source': source, 'start': start, 'end': end}

def parse_timeline(line, timeline):
    timeline['order'] = line.split(' ')

def parse_file(filename):
    print('Parsing {}'.format(filename))
    parts = {}
    with open(filename, 'r') as f:
        phase = ''
        phase_func = {'sources': parse_source_line,
                      'clips': parse_clip_line,
                      'timeline': parse_timeline}
        for line in f:
            if line[:3] == '===':
                phase = line.replace('=', '').rstrip()
                parts[phase] = {}
            else:
                try:
                    phase_func[phase](line.rstrip(), parts[phase])
                except KeyError:
                    print('{} is not a correct section header'.format(phase))
                    sys.exit(1)
    return parts

def duration(start, end):
    time_format = '%M:%S.%f'
    stime = datetime.datetime.strptime(start, time_format)
    etime = datetime.datetime.strptime(end, time_format)
    duration = etime - stime
    return str(duration)

if __name__ == '__main__':
    print('Super Simple Video Editor')
    if len(sys.argv) != 2:
        print('Incorrect usage, please pass ssve video format file')
    else:
        parts = parse_file(sys.argv[1])
        outname = os.path.splitext(sys.argv[1])[0]
        print(parts)

        if not os.path.exists('clips'):
            os.makedirs('clips')

        for clip_name in parts['clips']:
            clip = parts['clips'][clip_name]
            source = parts['sources'][clip['source']]
            dur = duration(clip['start'], clip['end'])
            command = 'ffmpeg -ss {start} -t {duration} -i "{source}" clips/{clip}.mp4'.format(source=source,
                                                                                                start=clip['start'],
                                                                                                duration=dur,
                                                                                                clip=clip_name)
            print(command)
            os.system(command)

        with open('clips/concat.txt', 'w') as f:
            for clip in parts['timeline']['order']:
                f.write("file '{}.mp4'\n".format(clip))
        command = 'ffmpeg -f concat -i clips/concat.txt {}.mp4'.format(outname)
        os.system(command)
