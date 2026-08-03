import librosa
import numpy as np
import yaml
import json

def analyze_sections_from_yaml(wav_path, yaml_path):
    # 1. Load and Parse YAML Configuration
    with open(yaml_path, 'r') as file:
        analysis_data = yaml.safe_load(file)

    track_meta = analysis_data['track_metadata']
    bpm = track_meta['bpm']

    # Extract the numerator from the time signature (e.g., "4" from "4/4")
    beats_per_bar = int(track_meta['time_signature'].split('/')[0])

    # Calculate absolute time in seconds per musical bar
    seconds_per_beat = 60.0 / bpm
    seconds_per_bar = seconds_per_beat * beats_per_bar

    # 2. Load Audio and Compute STFT
    print(f"Loading {wav_path} and computing STFT...")
    y, sr = librosa.load(wav_path, sr=None)
    n_fft = 4096
    stft = np.abs(librosa.stft(y, n_fft=n_fft))
    stft_db = librosa.amplitude_to_db(stft, ref=np.max)

    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    stft_times = librosa.frames_to_time(np.arange(stft_db.shape[1]), sr=sr)

    # Define standard frequency bands (Hz)
    bands = {
        'sub_20_60_hz': (20, 60),
        'low_60_250_hz': (60, 250),
        'mid_250_2k_hz': (250, 2000),
        'high_mid_2k_6k_hz': (2000, 6000),
        'high_6k_20k_hz': (6000, 20000)
    }

    # Structure the output data for JSON
    report_data = {'frequency_analysis': []}
    current_bar = 1

    # 3. Process Each Section Defined in YAML
    for section in analysis_data['arrangement']:
        section_name = section['section_name']
        duration_bars = section['duration_bars']

        start_time = (current_bar - 1) * seconds_per_bar
        end_time = start_time + (duration_bars * seconds_per_bar)

        # Locate STFT frames falling within this section's time boundary
        frame_indices = np.where((stft_times >= start_time) & (stft_times < end_time))[0]

        section_entry = {
            'section': section_name,
            'start_bar': current_bar,
            'duration_bars': duration_bars,
            'start_time_sec': round(float(start_time), 2),
            'end_time_sec': round(float(end_time), 2),
            'average_volumes_db': {}
        }

        if len(frame_indices) > 0:
            for band_key, (low_f, high_f) in bands.items():
                freq_indices = np.where((freqs >= low_f) & (freqs <= high_f))[0]
                if len(freq_indices) > 0:
                    # Average volume in dB for this band across this specific section
                    avg_db = np.mean(stft_db[np.ix_(freq_indices, frame_indices)])
                    section_entry['average_volumes_db'][band_key] = round(float(avg_db), 2)
                else:
                    section_entry['average_volumes_db'][band_key] = -100.0
        else:
            for band_key in bands:
                section_entry['average_volumes_db'][band_key] = -100.0

        report_data['frequency_analysis'].append(section_entry)

        # Advance the bar counter for the next section
        current_bar += duration_bars

    return report_data

# Execution Block
if __name__ == "__main__":
    # Replace with your actual file paths
    wav_file = "Lane8_Reviver.wav"
    input_yaml_file = "analysis.yaml"
    output_json_file = "frequency_report.json"

    try:
        report_dict = analyze_sections_from_yaml(wav_file, input_yaml_file)

        # 4. Write data to a new JSON file
        with open(output_json_file, 'w') as outfile:
            # indent=4 ensures the JSON is formatted clearly for human readability
            json.dump(report_dict, outfile, indent=4)

        print(f"Report successfully exported to {output_json_file}")

    except Exception as e:
        print(f"An error occurred: {e}")