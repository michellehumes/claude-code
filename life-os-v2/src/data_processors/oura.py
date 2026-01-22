"""
Oura Ring data processor for health tracking
"""

import pandas as pd
from datetime import datetime, timedelta
import json
import os


class OuraDataProcessor:
    """Process Oura Ring data exports"""

    def __init__(self, data_dir=None):
        self.data_dir = data_dir
        self.sleep_df = None
        self.activity_df = None
        self.readiness_df = None
        self.cycle_df = None
        self.temperature_df = None
        self.heartrate_df = None
        self.stress_df = None
        self.workout_df = None

    def load_all_data(self, data_dir=None):
        """Load all Oura data files from directory"""
        data_dir = data_dir or self.data_dir
        if not data_dir:
            raise ValueError("No data directory provided")

        files_loaded = []

        # Define file mappings
        file_mappings = [
            ('dailysleep.csv', 'sleep_df', self._process_sleep_data),
            ('dailyactivity.csv', 'activity_df', self._process_activity_data),
            ('dailyreadiness.csv', 'readiness_df', self._process_readiness_data),
            ('dailycyclephases.csv', 'cycle_df', self._process_cycle_data),
            ('temperature.csv', 'temperature_df', self._process_temperature_data),
            ('heartrate.csv', 'heartrate_df', self._process_heartrate_data),
            ('dailystress.csv', 'stress_df', self._process_stress_data),
            ('workout.csv', 'workout_df', self._process_workout_data),
        ]

        for filename, attr, processor in file_mappings:
            filepath = os.path.join(data_dir, filename)
            if os.path.exists(filepath):
                try:
                    # Oura uses semicolon delimiter
                    df = pd.read_csv(filepath, delimiter=';')
                    processed_df = processor(df)
                    setattr(self, attr, processed_df)
                    files_loaded.append(filename)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

        return files_loaded

    def _process_sleep_data(self, df):
        """Process daily sleep data"""
        # Rename columns if needed
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]

        # Parse date column
        if 'day' in df.columns:
            df['date'] = pd.to_datetime(df['day'])
        elif 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])

        # Parse JSON contributors if present
        if 'contributors' in df.columns:
            df = self._parse_contributors(df, 'contributors')

        return df

    def _process_activity_data(self, df):
        """Process daily activity data"""
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]

        if 'day' in df.columns:
            df['date'] = pd.to_datetime(df['day'])
        elif 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])

        return df

    def _process_readiness_data(self, df):
        """Process daily readiness data"""
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]

        if 'day' in df.columns:
            df['date'] = pd.to_datetime(df['day'])
        elif 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])

        # Parse JSON contributors if present
        if 'contributors' in df.columns:
            df = self._parse_contributors(df, 'contributors')

        return df

    def _process_cycle_data(self, df):
        """Process daily cycle phases data"""
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]

        if 'day' in df.columns:
            df['date'] = pd.to_datetime(df['day'])
        elif 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])

        return df

    def _process_temperature_data(self, df):
        """
        Process temperature data
        Aggregate minute-by-minute to daily averages
        """
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]

        # Parse timestamp
        if 'timestamp' in df.columns:
            df['datetime'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['datetime'].dt.date

            # Aggregate to daily
            daily_temp = df.groupby('date').agg({
                'temperature': ['mean', 'min', 'max', 'std']
            }).reset_index()

            daily_temp.columns = ['date', 'avg_temp', 'min_temp', 'max_temp', 'temp_std']
            return daily_temp

        return df

    def _process_heartrate_data(self, df):
        """
        Process heart rate data
        Aggregate to daily summaries
        """
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]

        # Parse timestamp
        if 'timestamp' in df.columns:
            df['datetime'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['datetime'].dt.date

            # Determine resting vs active hours (assume 11pm-7am is rest)
            df['hour'] = df['datetime'].dt.hour
            df['is_rest'] = (df['hour'] >= 23) | (df['hour'] < 7)

            # Aggregate to daily
            daily_hr = df.groupby('date').agg({
                'bpm': ['mean', 'min', 'max']
            }).reset_index()

            daily_hr.columns = ['date', 'avg_hr', 'min_hr', 'max_hr']

            # Calculate resting HR (average during rest hours)
            rest_hr = df[df['is_rest']].groupby('date')['bpm'].mean().reset_index()
            rest_hr.columns = ['date', 'resting_hr']

            daily_hr = daily_hr.merge(rest_hr, on='date', how='left')

            return daily_hr

        return df

    def _process_stress_data(self, df):
        """Process daily stress data"""
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]

        if 'day' in df.columns:
            df['date'] = pd.to_datetime(df['day'])
        elif 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])

        return df

    def _process_workout_data(self, df):
        """Process workout data"""
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]

        if 'start_datetime' in df.columns:
            df['date'] = pd.to_datetime(df['start_datetime']).dt.date

        return df

    def _parse_contributors(self, df, column):
        """Parse JSON contributors column into separate columns"""
        try:
            contributors = df[column].apply(
                lambda x: json.loads(x) if pd.notna(x) and x else {}
            )

            for key in ['deep_sleep', 'efficiency', 'latency', 'rem_sleep',
                        'restfulness', 'timing', 'total_sleep', 'activity_balance',
                        'body_temperature', 'hrv_balance', 'previous_day_activity',
                        'previous_night', 'recovery_index', 'resting_heart_rate',
                        'sleep_balance']:
                df[f'contrib_{key}'] = contributors.apply(lambda x: x.get(key, None))
        except Exception as e:
            print(f"Error parsing contributors: {e}")

        return df

    def get_sleep_data(self):
        """Get sleep data formatted for Google Sheets"""
        if self.sleep_df is None:
            return []

        data = []
        for _, row in self.sleep_df.iterrows():
            date = row.get('date', row.get('day', ''))
            if isinstance(date, pd.Timestamp):
                date = date.strftime('%m/%d/%Y')

            data.append([
                date,                                                  # Date
                row.get('score', ''),                                  # Sleep Score
                row.get('total_sleep_duration', '') / 3600 if row.get('total_sleep_duration') else '',  # Total Sleep (hrs)
                row.get('deep_sleep_duration', '') / 60 if row.get('deep_sleep_duration') else '',      # Deep Sleep (min)
                row.get('rem_sleep_duration', '') / 60 if row.get('rem_sleep_duration') else '',        # REM Sleep (min)
                row.get('light_sleep_duration', '') / 60 if row.get('light_sleep_duration') else '',    # Light Sleep (min)
                row.get('efficiency', ''),                             # Sleep Efficiency
                row.get('latency', '') / 60 if row.get('latency') else '',  # Sleep Latency (min)
                row.get('contrib_restfulness', ''),                    # Restfulness Score
                row.get('contrib_timing', ''),                         # Timing Score
                ''                                                     # Notes
            ])

        return data

    def get_activity_data(self):
        """Get activity data formatted for Google Sheets"""
        if self.activity_df is None:
            return []

        data = []
        for _, row in self.activity_df.iterrows():
            date = row.get('date', row.get('day', ''))
            if isinstance(date, pd.Timestamp):
                date = date.strftime('%m/%d/%Y')

            data.append([
                date,                                                  # Date
                row.get('score', ''),                                  # Activity Score
                row.get('steps', ''),                                  # Steps
                row.get('active_calories', ''),                        # Active Calories
                row.get('total_calories', ''),                         # Total Calories
                row.get('equivalent_walking_distance', ''),            # Distance (m)
                row.get('high_activity_time', '') / 60 if row.get('high_activity_time') else '',  # High Activity (min)
                row.get('medium_activity_time', '') / 60 if row.get('medium_activity_time') else '',  # Medium Activity (min)
                row.get('low_activity_time', '') / 60 if row.get('low_activity_time') else '',  # Low Activity (min)
                row.get('sedentary_time', '') / 3600 if row.get('sedentary_time') else '',  # Sedentary (hrs)
                row.get('inactivity_alerts', ''),                      # Inactivity Alerts
                row.get('meet_daily_targets', ''),                     # Meet Daily Targets %
                row.get('move_every_hour', ''),                        # Move Every Hour %
                row.get('training_volume', '')                         # Training Volume Score
            ])

        return data

    def get_readiness_data(self):
        """Get readiness data formatted for Google Sheets"""
        if self.readiness_df is None:
            return []

        data = []
        for _, row in self.readiness_df.iterrows():
            date = row.get('date', row.get('day', ''))
            if isinstance(date, pd.Timestamp):
                date = date.strftime('%m/%d/%Y')

            data.append([
                date,                                                  # Date
                row.get('score', ''),                                  # Readiness Score
                row.get('contrib_recovery_index', ''),                 # Recovery Index
                row.get('contrib_sleep_balance', ''),                  # Sleep Balance
                row.get('contrib_previous_day_activity', ''),          # Previous Day Activity
                row.get('contrib_activity_balance', ''),               # Activity Balance
                row.get('contrib_body_temperature', ''),               # Body Temperature
                row.get('contrib_resting_heart_rate', ''),             # Resting Heart Rate
                row.get('contrib_hrv_balance', ''),                    # HRV Balance
                ''                                                     # Notes
            ])

        return data

    def get_cycle_data(self):
        """Get cycle data formatted for Google Sheets"""
        if self.cycle_df is None:
            return []

        data = []
        for _, row in self.cycle_df.iterrows():
            date = row.get('date', row.get('day', ''))
            if isinstance(date, pd.Timestamp):
                date = date.strftime('%m/%d/%Y')

            data.append([
                date,                                                  # Date
                row.get('cycle_day', ''),                              # Day of Cycle
                row.get('phase', ''),                                  # Cycle Phase
                row.get('cycle_id', ''),                               # Oura Cycle ID
                '',                                                    # Manual Cycle # (linked)
                '',                                                    # Period Confirmed
                '',                                                    # Ovulation Confirmed
                ''                                                     # Discrepancy Notes
            ])

        return data

    def get_temperature_data(self):
        """Get daily temperature data formatted for Google Sheets"""
        if self.temperature_df is None:
            return []

        data = []
        baseline_temp = None

        for _, row in self.temperature_df.iterrows():
            date = row.get('date', '')
            if isinstance(date, pd.Timestamp):
                date = date.strftime('%m/%d/%Y')

            avg_temp = row.get('avg_temp', '')

            # Calculate baseline if not set (use first 5 days average)
            if baseline_temp is None and len(data) < 5 and avg_temp:
                baseline_temp = avg_temp

            # Calculate deviation
            deviation = avg_temp - baseline_temp if baseline_temp and avg_temp else ''

            # Determine trend based on previous row
            if len(data) > 0 and avg_temp and data[-1][1]:
                prev_temp = data[-1][1]
                if avg_temp > prev_temp + 0.1:
                    trend = "↑"
                elif avg_temp < prev_temp - 0.1:
                    trend = "↓"
                else:
                    trend = "→"
            else:
                trend = "→"

            data.append([
                date,                                                  # Date
                avg_temp,                                              # Avg Nighttime Temp
                deviation,                                             # Deviation from Baseline
                trend,                                                 # Temp Trend
                '',                                                    # Cycle Day (linked)
                '',                                                    # Cycle Phase (linked)
                '',                                                    # Predicted Ovulation Day
                'N',                                                   # BBT Shift Detected
                'N',                                                   # Fever Alert
                ''                                                     # Notes
            ])

        return data

    def get_heartrate_data(self):
        """Get daily heart rate data formatted for Google Sheets"""
        if self.heartrate_df is None:
            return []

        data = []
        for _, row in self.heartrate_df.iterrows():
            date = row.get('date', '')
            if isinstance(date, pd.Timestamp):
                date = date.strftime('%m/%d/%Y')

            # Determine trend
            if len(data) > 0 and row.get('resting_hr') and data[-1][1]:
                prev_hr = data[-1][1]
                current_hr = row.get('resting_hr')
                if current_hr > prev_hr + 2:
                    trend = "↑"
                elif current_hr < prev_hr - 2:
                    trend = "↓"
                else:
                    trend = "→"
            else:
                trend = "→"

            data.append([
                date,                                                  # Date
                row.get('resting_hr', ''),                             # Avg Resting HR
                row.get('min_hr', ''),                                 # Lowest Nighttime HR
                row.get('avg_hr', ''),                                 # Avg Daytime HR
                row.get('max_hr', ''),                                 # Max HR
                '',                                                    # HRV Score (if available)
                trend,                                                 # HRV Trend
                '',                                                    # Cycle Day (linked)
                '',                                                    # Stress Level
                ''                                                     # Notes
            ])

        return data

    def get_stress_data(self):
        """Get daily stress data formatted for Google Sheets"""
        if self.stress_df is None:
            return []

        data = []
        for _, row in self.stress_df.iterrows():
            date = row.get('date', row.get('day', ''))
            if isinstance(date, pd.Timestamp):
                date = date.strftime('%m/%d/%Y')

            # Determine stress level category
            stress_score = row.get('stress_high', 0)
            if stress_score > 80:
                stress_level = "Very High"
            elif stress_score > 50:
                stress_level = "High"
            elif stress_score > 20:
                stress_level = "Medium"
            else:
                stress_level = "Low"

            data.append([
                date,                                                  # Date
                row.get('day_summary', ''),                            # Daily Stress Score
                stress_level,                                          # Daytime Stress Level
                row.get('stress_high', ''),                            # Stress Duration (min)
                row.get('recovery_high', ''),                          # Recovery Time (min)
                '',                                                    # Resilience Score
                '',                                                    # Stressful Periods
                '',                                                    # Calm Periods
                '',                                                    # Notes
                ''                                                     # Triggers
            ])

        return data

    def get_health_dashboard_summary(self):
        """Get summary data for Oura Health Dashboard"""
        summary = {
            'sleep_days': len(self.sleep_df) if self.sleep_df is not None else 0,
            'activity_days': len(self.activity_df) if self.activity_df is not None else 0,
            'readiness_days': len(self.readiness_df) if self.readiness_df is not None else 0,
            'cycle_days': len(self.cycle_df) if self.cycle_df is not None else 0,
        }

        # Get latest scores
        if self.sleep_df is not None and len(self.sleep_df) > 0:
            summary['latest_sleep_score'] = self.sleep_df.iloc[-1].get('score', 0)
            summary['avg_sleep_score_7d'] = self.sleep_df.tail(7)['score'].mean() if 'score' in self.sleep_df.columns else 0

        if self.activity_df is not None and len(self.activity_df) > 0:
            summary['latest_activity_score'] = self.activity_df.iloc[-1].get('score', 0)
            summary['total_steps_7d'] = self.activity_df.tail(7)['steps'].sum() if 'steps' in self.activity_df.columns else 0

        if self.readiness_df is not None and len(self.readiness_df) > 0:
            summary['latest_readiness_score'] = self.readiness_df.iloc[-1].get('score', 0)
            summary['avg_readiness_7d'] = self.readiness_df.tail(7)['score'].mean() if 'score' in self.readiness_df.columns else 0

        return summary

    @staticmethod
    def generate_sample_sleep_data(days=30):
        """Generate sample sleep data for testing"""
        import random

        data = []
        today = datetime.now()

        for i in range(days):
            date = today - timedelta(days=days-i-1)

            # Generate realistic sleep scores
            base_score = random.randint(65, 95)
            total_sleep = random.uniform(6, 9)  # hours
            deep_sleep = random.uniform(45, 120)  # minutes
            rem_sleep = random.uniform(60, 150)  # minutes
            light_sleep = (total_sleep * 60) - deep_sleep - rem_sleep
            efficiency = random.randint(80, 98)
            latency = random.randint(5, 30)

            data.append([
                date.strftime('%m/%d/%Y'),
                base_score,
                round(total_sleep, 1),
                round(deep_sleep, 0),
                round(rem_sleep, 0),
                round(light_sleep, 0),
                efficiency,
                latency,
                random.randint(70, 95),  # Restfulness
                random.randint(60, 100),  # Timing
                ''
            ])

        return data

    @staticmethod
    def generate_sample_activity_data(days=30):
        """Generate sample activity data for testing"""
        import random

        data = []
        today = datetime.now()

        for i in range(days):
            date = today - timedelta(days=days-i-1)

            steps = random.randint(3000, 15000)
            active_cal = random.randint(200, 800)
            total_cal = active_cal + random.randint(1500, 2000)

            data.append([
                date.strftime('%m/%d/%Y'),
                random.randint(50, 100),      # Activity Score
                steps,
                active_cal,
                total_cal,
                steps * 0.762,                # Distance (m)
                random.randint(0, 60),        # High activity
                random.randint(15, 90),       # Medium activity
                random.randint(60, 180),      # Low activity
                random.uniform(6, 12),        # Sedentary (hrs)
                random.randint(0, 3),         # Inactivity alerts
                random.randint(50, 100),      # Meet targets %
                random.randint(50, 100),      # Move every hour %
                random.randint(0, 50)         # Training volume
            ])

        return data

    @staticmethod
    def generate_sample_readiness_data(days=30):
        """Generate sample readiness data for testing"""
        import random

        data = []
        today = datetime.now()

        for i in range(days):
            date = today - timedelta(days=days-i-1)

            data.append([
                date.strftime('%m/%d/%Y'),
                random.randint(50, 100),      # Readiness Score
                random.randint(60, 100),      # Recovery Index
                random.randint(60, 100),      # Sleep Balance
                random.randint(60, 100),      # Previous Day Activity
                random.randint(60, 100),      # Activity Balance
                random.randint(60, 100),      # Body Temperature
                random.randint(60, 100),      # Resting HR
                random.randint(60, 100),      # HRV Balance
                ''
            ])

        return data

    @staticmethod
    def generate_sample_cycle_data(days=90):
        """Generate sample cycle data for testing"""
        data = []
        today = datetime.now()

        cycle_day = 1
        cycle_id = 1
        cycle_length = 28

        for i in range(days):
            date = today - timedelta(days=days-i-1)

            # Determine phase
            if cycle_day <= 5:
                phase = "Menstrual"
            elif cycle_day <= 13:
                phase = "Follicular"
            elif cycle_day <= 16:
                phase = "Ovulation"
            else:
                phase = "Luteal"

            data.append([
                date.strftime('%m/%d/%Y'),
                cycle_day,
                phase,
                f"CYCLE_{cycle_id}",
                '',
                'Y' if cycle_day <= 5 else 'N',
                'Y' if 13 <= cycle_day <= 16 else 'N',
                ''
            ])

            cycle_day += 1
            if cycle_day > cycle_length:
                cycle_day = 1
                cycle_id += 1
                cycle_length = 28 + (cycle_id % 3 - 1)  # Vary cycle length slightly

        return data
