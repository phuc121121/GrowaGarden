# ApplySpark: 2-Minute Cinematic Prop Video Script (v3)

**Format:** 16:9, 2:00, cinematic business-proposal style, music-led, subtitles only for 5 short lines.
**Tagline:** Thắp sáng tiềm năng hồ sơ
**Palette:** navy and gold. Cool, dark grade while Khoi struggles; warm gold once he finds ApplySpark.

## Story

Khoi loves the idea of studying abroad but is lost: which clubs to join, which extracurriculars matter, and what path to follow. His parent tells him to go and ask about it. At a consultancy centre he is shown a price and walks away sad. His friend Kien then suggests ApplySpark. He tries it and finds a free, clear path.

## Cast

| Character | Role in this version |
|---|---|
| **Khoi** | Student, loves study abroad but has no path |
| **Parent** | Unnamed parent (Kien's old role is now a friend) who tells him to go ask about it |
| **Tuan Minh** | Study-abroad consultancy centre advisor, shows the price |
| **Kien** | Khoi's friend, suggests ApplySpark |
| **Phuc** | Homeroom teacher, optional cameo (not in this cut) |

## Voicelines (5 total, subtitles only)

| ID | Speaker | Vietnamese | English |
|---|---|---|---|
| V1 | Khoi | "Mình muốn đi du học… nhưng chưa biết bắt đầu từ đâu." | "I want to study abroad... but I don't know where to start." |
| V2 | Parent | "Con thích du học thì đi hỏi thử xem." | "If you like studying abroad, go and ask." |
| V3 | Kien | "Thử ApplySpark đi. Miễn phí, tìm trường, CLB, hạn nộp." | "Try ApplySpark. It's free: schools, clubs, deadlines." |
| V4 | Khoi | "Giờ mình biết mình đang đi đâu." | "Now I know where I'm headed." |

(The price scene has no spoken line; the quote card on the table carries it.)

## Shot list

### Act 1: The struggle (0:00-0:38)
Copied from the Firstship reference: opening doors reveal, foreground blur, push-ins, dutch-angle screen.
| Time | Shot | Camera |
|---|---|---|
| 0:00-0:05 | Doors slide open to reveal Khoi at his desk | Push-in, doors animate apart |
| 0:05-0:10 | Khoi at his laptop, blurred silhouette in the foreground | Over-the-shoulder, slow dolly |
| 0:10-0:16 | Club-flyer noticeboard, Khoi small on the left: "Câu lạc bộ? Hoạt động ngoại khóa?" | Pan right-to-left, push-in |
| 0:16-0:22 | Khoi close-up, **V1** | Slow push-in |
| 0:22-0:27 | Top-down desk with sticky notes and papers | Slow rotation and push |
| 0:27-0:33 | Tilted board: "Du học: bắt đầu từ đâu?" with Chọn nước? Chọn ngành? Hoạt động ngoại khóa? Học bổng? Hạn nộp? | Dutch angle, push-in |
| 0:33-0:38 | Navy card: "Muốn du học. Chưa có lộ trình." | Slow zoom |

### Act 2: The price (0:38-1:07)
| Time | Shot | Camera |
|---|---|---|
| 0:38-0:45 | Parent at the kitchen table, **V2** | Slow dolly toward the parent |
| 0:45-0:51 | Tuan Minh's consultancy office, world map behind him | Wide, push-in |
| 0:51-0:57 | Khoi sits across from Tuan Minh | Over-the-shoulder, blurred foreground |
| 0:57-1:02 | Insert: price sheet "?,???,??? VND" (no real figure shown, a sourced price needs checking first) | Push-in |
| 1:02-1:07 | Khoi's sad face, close-up | Slow push, cool grade |

### Act 3: The turn (1:07-1:54)
| Time | Shot | Camera |
|---|---|---|
| 1:07-1:14 | Khoi and his friend Kien on the school steps, laptop between them, **V3** | Slow push toward the laptop, warm light |
| 1:14-1:19 | ApplySpark homepage: "Thắp sáng tiềm năng hồ sơ" | Tilted UI card, push-in |
| 1:19-1:25 | University page: rankings, costs, deadlines | Push-in with slight rotation |
| 1:25-1:31 | Saved list, deadline timeline, roadmap | Pan right, push-in |
| 1:31-1:37 | Profile analyzer: "Gợi ý hồ sơ, không phải cam kết đậu" | Push toward the score |
| 1:37-1:42 | Tools: Clubs, Competitions, Internships, Alumni, Archive, Teams | Pull-in |
| 1:42-1:48 | Agencies directory + "Basic miễn phí" | Slow push |
| 1:48-1:54 | Khoi walks out through a golden door, **V4** | Low angle, pull-back |

### End card (1:54-2:00)
Blue card: logo, "Thắp sáng tiềm năng hồ sơ", applysparkvn.com. Music resolves.

## Sound
- Low ambient pad, clock ticks while Khoi struggles, a kick pulse builds from 1:07, chimes as the saved list and deadlines appear, a swell to the logo hit.

## Fact guardrails (ApplySpark dossier)
- The price sheet shows "?,???,???". Any real consultancy price (e.g. 50-100m VND) is a proposal claim needing evidence.
- Basic is free. Premium (49,000 VND/month) and VIP (149,000 VND/month) are "Coming soon", so they are not shown as live.
- The 22 Premium/VIP accounts are test/complimentary access, not paying users.
- The profile score is guidance, not an admissions probability.
- Tools shown (Clubs, Competitions, Internships, Alumni, Archive, Teams, Agencies) come from the October 2026 homepage list.
- Don't show emails or phone numbers.

## Build
`ApplySpark_Prop_Video.mp4`: 960x540, 24 fps, synthesized score, subtitles only (no recorded voice).
Rebuild: `python3 render_audio.py && python3 render_video.py silent.mp4`, then mux with ffmpeg.
