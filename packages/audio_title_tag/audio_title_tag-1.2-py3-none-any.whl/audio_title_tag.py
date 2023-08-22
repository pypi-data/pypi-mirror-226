import os
import sys
import eyed3
from mutagen.flac import FLAC

# 支持的音频文件格式
SUPPORTED_FORMATS = ['.mp3', '.flac']

# 获取指定文件夹中的所有音频文件（支持的格式）
def get_audio_files(folder):
    audio_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if any(file.lower().endswith(ext) for ext in SUPPORTED_FORMATS):
                audio_files.append(os.path.join(root, file))
    return audio_files

# 更新音频文件的标题
def update_audio_metadata(file_path):
    _, extension = os.path.splitext(file_path)

    try:
        if extension.lower() == '.mp3':
            # 更新MP3文件的元数据
            audio = eyed3.load(file_path)
            if audio.tag:
                filename = os.path.splitext(os.path.basename(file_path))[0]
                audio.tag.title = filename
                audio.tag.save(version=eyed3.id3.ID3_V2_3)  # 强制设置为 ID3 v2.3
                print(f"已更新 {file_path} 的元数据")
        elif extension.lower() == '.flac':
            # 更新FLAC文件的元数据
            audio = FLAC(file_path)
            if audio:
                filename = os.path.splitext(os.path.basename(file_path))[0]
                audio['title'] = filename
                audio.save()
                print(f"已更新 {file_path} 的元数据")
        else:
            print(f"不支持的格式或无法解析的文件: {file_path}")
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误: {e}")
        raise  # 重新引发异常，终止脚本执行


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python update_title_tag.py <文件夹路径>")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print("无效的文件夹路径")
        sys.exit(1)

    audio_files = get_audio_files(folder_path)

    error_files = []

    for audio_file in audio_files:
        try:
            update_audio_metadata(audio_file)
        except:
            error_files.append(audio_file)

    if error_files:
        print("以下文件处理时发生错误:")
        for error_file in error_files:
            print(error_file)
    else:
        print("所有文件处理完成，没有发生错误。")
