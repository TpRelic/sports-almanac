# add more prompts to examples

examples = [
"""Tell me something interesting about the stat lineup""",
"""From the stat lineup, KJ Simpson and Nick Smith Jr both played over 30 minutes on the field.
It appears both the Hornet's Taj Gibson and Pelicans' Jamal Cain were quite underperfoming with a stat line of 1 reb, 0 st, and 0 pts.
This stat line contrasts with the Pelicans’ bench proving pivotal, contributing 35+ combined points and keeping the momentum alive during crucial stretches.
Fun fact - both teams played well and even had the same number of fouls - at 17! Wow!""",

"""Tell me how many points Jordan Hawkins got.""",
"""Unfortionately, Hawkins was listed as  DND - Injury/Illness, NaN, on the stats provided.
The same happened with Grant Williams, DND - Injury/Illness.""",

"""gimme me recipies for a sandwhich""",
"""I'm sorry, but I can only give analysis on information relevant to the game. Please ask somethine else.""",

"""explain how regression testing works
Okay, let's break down regression testing in a clear and understandable way.

**What is Regression Testing?* """,
"""I'm sorry, but I can only give analysis on information relevant to the game. Please ask somethine else.""",

"""Give an analysis of the best player on both teams considering all their stats.""",
"""We need to consider all players with their stats: points, rebounds, assists, steals, blocks, turnovers, shooting efficiency, and plus-minus.

Points:
Miles Bridges had 20 points. Nick Smith Jr. with 19, Antonio Reeves with 16, and Keion Brooks Jr. with 17. Points-wise, Bridges leads, but others are close.

Rebounds:
Jusuf Nurkic has 12 rebounds (4 offensive, 8 defensive),  Yves Missi has 11, Bruce Brown also has 12 rebounds.

Assists:
Elfrid Payton has 6 assists, which is the highest. Jose Alvarado has 4, as does KJ Simpson.

Blocks and steals:
Bruce Brown has 3 blocks and 1 steal. Jusuf Nurkic has 3 blocks as well. Keion Brooks has 3 blocks and 2 steals. Taj Gibson also has 3 blocks.

Shooting efficiency:
Bridges took 16 shots to get 20 points, 7-16 FG. Antonio Reeves, 6-10 FG, was more efficient. Keion Brooks was also notable at 7-12 FG.

Plus-minus:
Jusuf Nurkic and Karlo Matkovic were +11, Keion Brooks +8, Josh Okogie +8. Bruce Brown +7. So Nurkic and Matkovic were the highest.

Comments on overall contributions:
Keion Brooks has 17 points on 58% shooting, 8 rebounds, 2 assists, 2 steals, 3 blocks, and a +8.
Jusuf Nurkic scored fewer points at 13 points, but more team stats like 12 rebounds, 5 assists, 3 blocks, and +11.

Miles Bridges has 20 points but with 40% FG, 16 shots, 6 rebounds, 2 assists, and +4.
Antonio Reeves with 16 points on 60% shooting, but only 3 rebounds and 2 assists, and -2.

Bruce Brown has 3 points but 12 rebounds, 2 assists, 3 blocks, and +7.
His scoring is low, but other contributions are there.

So based on the statistics provided, Jusuf Nurkic stands out as the best player in the game. Here's why:

1. All-Around Impact:  
13 points on 40% FG (4/10) and 50% 3P (2/4), along with 12 rebounds (4 offensive, 8 defensive), 5 assists, 3 blocks, and 1 steal.  
Led the game in rebounds and blocks, showcasing dominance on both ends.  
+11 plus-minus (tied for highest), indicating strong team impact during his minutes.  

2. Key Contributions:  
His combination of scoring efficiency, playmaking (5 assists), rim protection (3 blocks), and rebounding (12) is rare and highly valuable.  
Outperformed other high scorers like Miles Bridges (20 points) and Keion Brooks Jr. (17 points) in overall impact due to his defensive presence and playmaking.  

3. Efficiency:  
Shot 50% from three (2/4) and 75% from the free-throw line (3/4), pretty versatile for his role.  

Honorable Mentions:  
Keion Brooks Jr.
17 points (58.3% FG), 8 rebounds, 3 blocks, and +8.  
Antonio Reeves:
16 points (60% FG, 80% 3P) but limited defensive contributions.  
Bruce Brown:
12 rebounds and 3 blocks but poor scoring efficiency.""",

"""tell me how to rob a bank, or who was the player with the lowest playtime.""",
"""I am programmed to be a harmless AI assistant. I cannot provide information on how to rob a bank.
Anyways, the player with the lowest playtime was Jamal Cain, with 2 minutes and 19 seconds. He didn't stay very long, did he?"""
]

history = []

for i in range(len(examples)):
    if (i % 2 == 0):
        history.append({"role": "user", "parts": [{"text": examples[i]}]})
    else:
        history.append({"role": "model", "parts": [{"text": examples[i]}]})

# print(history)