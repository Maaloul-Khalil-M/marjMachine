# YASB Time Period Widget - Enhanced Edition 🌞🌙

A **highly customizable time-aware widget** for YASB that shows what part of your day you're in with rich visual feedback.

## ✨ Key Features

- 🎨 **External JSON configuration** - Easily customize periods without editing code
- 📊 **Progress tracking** - See how far you are through the current period
- 🖱️ **Multiple display modes** - Toggle between compact and detailed views
- 💡 **Rich tooltips** - Hover to see detailed information including progress bar
- 🔧 **Quick config editing** - Middle-click to edit time periods
- ⚡ **Lightweight** - Pure Node.js, no external dependencies

## 📋 What You Get

### Display Modes (Click to Toggle)

**Mode 1: Icon Only**
```
🌻
```

**Mode 2: Icon + Time Remaining**
```
🌻 5h 23m
```

### Tooltip (Hover to See)
```
Morning - Peak Focus Time
████████░░ 78%
Remaining: 3h 15m
Next: 🪴 Afternoon
```

## 📦 Files Structure

```
├── time_period.js          # Main script
├── time_periods.json       # Configuration (easy to edit!)
└── yasb config additions   # Add to your YASB config
```

## 🚀 Installation

### 1. Create the files

Save these three files in a folder (e.g., `C:\yasb-scripts\time-period\`):

**time_period.js** - The main script (provided)
**time_periods.json** - Your time period configuration (provided)

### 2. Customize your time periods

Edit `time_periods.json` to match your daily rhythm:

```json
{
  "periods": [
    {
      "name": "Deep Focus",
      "icon": "🔥",
      "start": 9,
      "end": 12,
      "description": "Maximum Productivity"
    },
    {
      "name": "Lunch Break",
      "icon": "🍽️",
      "start": 12,
      "end": 13,
      "description": "Recharge Time"
    }
  ]
}
```

### 3. Add to YASB config

Add the widget configuration to your `config.yaml`:

```yaml
time_period:
  type: "yasb.custom.CustomWidget"
  options:
    label: "<span>{data[icon]}</span>"
    label_alt: "<span>{data[icon]}</span> {data[remaining]}"
    class_name: "time-period-widget"
    tooltip: true
    tooltip_label: "{data[name]} - {data[description]}\n{data[progressBar]} {data[progress]}%\nRemaining: {data[remaining]}\nNext: {data[nextIcon]} {data[nextName]}"
    exec_options:
      run_cmd: "node C:\\yasb-scripts\\time-period\\time_period.js"
      run_interval: 60000
      return_format: "json"
      use_shell: false
    callbacks:
      on_left: "toggle_label"
      on_middle: "exec cmd /c notepad C:\\yasb-scripts\\time-period\\time_periods.json"
      on_right: "toggle_label"
```

### 4. Add styles (optional)

Add to your `styles.css` for better appearance:

```css
.time-period-widget {
  margin: 0 8px;
}

.time-period-widget .widget-container {
  background-color: rgba(30, 30, 30, 0.8);
  border-radius: 8px;
  padding: 4px 12px;
}

.time-period-widget .label {
  font-size: 16px;
}
```

### 5. Restart YASB

Restart YASB to load the new widget.

## 🎮 Controls

| Action       | Behavior                           |
|--------------|------------------------------------|
| Left click   | Toggle between icon and icon+time  |
| Right click  | Toggle between icon and icon+time  |
| Middle click | Open config file for editing       |
| Hover        | Show detailed tooltip with progress|

## 🎨 Customization Ideas

### Example 1: Work-Focused Schedule
```json
{
  "periods": [
    {"name": "Sleep", "icon": "😴", "start": 0, "end": 7, "description": "Rest"},
    {"name": "Morning Routine", "icon": "☕", "start": 7, "end": 9, "description": "Wake Up"},
    {"name": "Deep Work", "icon": "🔥", "start": 9, "end": 12, "description": "Maximum Focus"},
    {"name": "Lunch", "icon": "🍽️", "start": 12, "end": 13, "description": "Break Time"},
    {"name": "Meetings", "icon": "👥", "start": 13, "end": 15, "description": "Collaboration"},
    {"name": "Focus Block", "icon": "💪", "start": 15, "end": 18, "description": "Second Wind"},
    {"name": "Evening", "icon": "🌆", "start": 18, "end": 22, "description": "Wind Down"},
    {"name": "Night", "icon": "🌙", "start": 22, "end": 24, "description": "Relax"}
  ]
}
```

### Example 2: Creative/Freelancer Schedule
```json
{
  "periods": [
    {"name": "Sleep", "icon": "💤", "start": 2, "end": 10, "description": "Deep Rest"},
    {"name": "Slow Start", "icon": "🌅", "start": 10, "end": 12, "description": "Wake Gently"},
    {"name": "Creative Peak", "icon": "🎨", "start": 12, "end": 17, "description": "Best Work"},
    {"name": "Break", "icon": "☕", "start": 17, "end": 18, "description": "Recharge"},
    {"name": "Night Owl", "icon": "🦉", "start": 18, "end": 2, "description": "Late Focus"}
  ]
}
```

### Example 3: Student Schedule
```json
{
  "periods": [
    {"name": "Sleep", "icon": "😴", "start": 23, "end": 7, "description": "Rest"},
    {"name": "Morning", "icon": "☀️", "start": 7, "end": 8, "description": "Get Ready"},
    {"name": "Classes", "icon": "📚", "start": 8, "end": 15, "description": "Learning"},
    {"name": "Study Time", "icon": "✏️", "start": 15, "end": 19, "description": "Homework"},
    {"name": "Free Time", "icon": "🎮", "start": 19, "end": 23, "description": "Relax"}
  ]
}
```

## 🔧 Advanced Features

### JSON Structure Explained

```json
{
  "name": "Morning",        // Period name (shown in tooltip)
  "icon": "🌻",            // Emoji shown in widget
  "start": 8,              // Start hour (24-hour format)
  "end": 14,               // End hour (24-hour format)
  "description": "Focus"   // Description (shown in tooltip)
}
```

### Midnight-Crossing Periods

The script handles periods that cross midnight automatically:
```json
{"name": "Night", "icon": "🌙", "start": 19, "end": 1, "description": "Evening"}
```
This means: 19:00 (7 PM) → 01:00 (1 AM next day)

## 📊 Output Data Structure

The script outputs JSON with these fields:

```json
{
  "icon": "🌻",
  "name": "Morning",
  "description": "Peak Focus Time",
  "remaining": "3h 15m",
  "progress": 67,
  "progressBar": "████████░",
  "nextIcon": "🪴",
  "nextName": "Afternoon",
  "timeUntilNext": "3h 15m"
}
```

You can use any of these in your label or tooltip!

## 🛠️ Troubleshooting

**Widget shows "⏰" with error:**
- Check that `time_periods.json` is in the same folder as `time_period.js`
- Verify the JSON syntax is valid
- Ensure at least one period covers the current hour

**Progress bar looks weird:**
- Use a monospace font in your styles
- Ensure your terminal/bar supports Unicode block characters

**Widget not updating:**
- Check the `run_interval` setting (60000 = 1 minute)
- Restart YASB after config changes
- Check YASB console for errors

**Can't edit config with middle click:**
- Update the path in the `on_middle` callback
- Make sure Notepad is available (or change to your preferred editor)

## 💡 Tips

1. **Start simple** - Use 4-6 periods initially, add more as needed
2. **Match your energy** - Align periods with your natural energy cycles
3. **Use meaningful icons** - Pick emojis that instantly convey the period's vibe
4. **Test your config** - Run the script manually first: `node time_period.js`
5. **Backup your config** - Keep a copy of `time_periods.json` before editing

## 🎯 Why Use This?

- **Reduces time anxiety** - Focus on phases, not exact minutes
- **Encourages natural rhythms** - Work with your energy, not against it
- **Simple awareness** - Quick glance = instant context
- **Highly personal** - Customize to your exact schedule
- **No overhead** - Lightweight, runs locally, no APIs

---

**Made with ❤️ for YASB users who want human-friendly time awareness**

---

Since you wanted easy mode switching, you can:

1. **Create multiple JSON files**:
   - `time_periods_work.json`
   - `time_periods_weekend.json`
   - `time_periods_creative.json`

2. **Switch between them** by changing the path in the script, OR

3. **Create separate widgets** for different modes:
```yaml
time_period_work:
  # ... points to time_periods_work.json

time_period_weekend:
  # ... points to time_periods_weekend.json
```

The comprehensive README includes multiple example schedules (work-focused, creative/freelancer, student) that you can use as starting points!

Would you like me to add any other features or create a script to switch between different config files automatically?