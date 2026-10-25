import json, re, sys

OUT = "/Users/kaneki/Desktop/workspace/Projects - Scrap/lorelines/research/apex-legends.json"
W = "https://apexlegends.wiki.gg/wiki/"
EA = "https://www.ea.com/games/apex-legends/apex-legends/characters-hub/"

LEGENDS = {  # slug: (wiki page, ea slug)
    "bloodhound": "Bloodhound", "gibraltar": "Gibraltar", "lifeline": "Lifeline", "pathfinder": "Pathfinder",
    "wraith": "Wraith", "bangalore": "Bangalore", "caustic": "Caustic", "mirage": "Mirage", "octane": "Octane",
    "wattson": "Wattson", "crypto": "Crypto", "revenant": "Revenant", "loba": "Loba", "rampart": "Rampart",
    "horizon": "Horizon", "fuse": "Fuse", "valkyrie": "Valkyrie", "seer": "Seer", "ash": "Ash",
    "mad-maggie": "Mad Maggie", "newcastle": "Newcastle", "vantage": "Vantage", "catalyst": "Catalyst",
    "ballistic": "Ballistic", "conduit": "Conduit", "alter": "Alter", "sparrow": "Sparrow", "axle": "Axle",
}

sources = [
    {"key": "wiki-timeline", "url": W + "Timeline", "title": "Timeline", "publisher": "wiki"},
]
for s, n in LEGENDS.items():
    sources.append({"key": "wiki-" + s, "url": W + n.replace(" ", "_") + "_(character)", "title": n + " (character)", "publisher": "wiki"})
    sources.append({"key": "ea-" + s, "url": EA + s, "title": n + " - Apex Legends Characters (official bio)", "publisher": "official"})
for key, page in [
    ("wiki-mercenary-syndicate", "Mercenary Syndicate"), ("wiki-kuben-blisk", "Kuben Blisk"),
    ("wiki-torres-silva", "Torres Silva"), ("wiki-minor-characters", "Minor characters"),
    ("wiki-kings-canyon", "Kings Canyon"), ("wiki-worlds-edge", "World's Edge"), ("wiki-olympus", "Olympus"),
    ("wiki-storm-point", "Storm Point"), ("wiki-broken-moon", "Broken Moon"), ("wiki-e-district", "E-District"),
    ("wiki-frontier-war", "Frontier War"), ("wiki-imc", "Interstellar Manufacturing Corporation"),
    ("wiki-apex-games", "Apex Games"), ("wiki-apex-predators", "Apex Predators"), ("wiki-project-iris", "Project Iris"),
    ("wiki-hammond-robotics", "Hammond Robotics"), ("wiki-shadow-revenant", "Shadow Revenant"),
    ("wiki-voidwalker-wraith", "Voidwalker Wraith"), ("wiki-amer-singh", "Amer Singh"), ("wiki-void", "Void"),
    ("wiki-season-25", "Season 25"), ("wiki-season-29", "Season 29"),
]:
    sources.append({"key": key, "url": W + page.replace(" ", "_"), "title": page, "publisher": "wiki"})
sources += [
    {"key": "ea-upheaval-patch-notes", "url": "https://www.ea.com/games/apex-legends/apex-legends/news/upheaval-patch-notes", "title": "Apex Legends: Upheaval Patch Notes (new Legend: Alter)", "publisher": "official"},
    {"key": "ea-shockwave-patch-notes", "url": "https://www.ea.com/games/apex-legends/apex-legends/news/shockwave-patch-notes", "title": "Apex Legends: Shockwave Patch Notes (E-District)", "publisher": "official"},
    {"key": "ea-prodigy-patch-notes", "url": "https://www.ea.com/games/apex-legends/apex-legends/news/prodigy-patch-notes", "title": "Apex Legends: Prodigy Patch Notes (Sparrow)", "publisher": "official"},
    {"key": "ea-overclocked-patch-notes", "url": "https://www.ea.com/games/apex-legends/apex-legends/news/overclocked-patch-notes", "title": "Apex Legends: Overclocked Patch Notes (new Legend: Axle)", "publisher": "official"},
]

timelines = [
    {"slug": "outlands", "name": "The Outlands (Apex Games reality)", "kind": "canon", "parent": None, "branch_note": None,
     "description": "The main reality of Apex Legends, shared with Titanfall: the Frontier Militia wins the Frontier War, the IMC withdraws, and the Mercenary Syndicate runs the Apex Games in the Outlands from 2729 on."},
    {"slug": "imc-victory", "name": "IMC-Victory Dimension (Wraith's home reality)", "kind": "alternate", "parent": "outlands",
     "branch_note": "Diverges at the Frontier War: in this reality the IMC defeats the Frontier Militia and still operates on Solace in 2727. Wraith (Renee Blasey) is from here and crosses into the main reality in 2727.",
     "description": "The parallel world where the IMC won the Frontier War. Its ARES Division ran Project Wraith at Singh Labs, where its Renee Blasey lost her memory and was imprisoned until her main-reality counterpart, the Voidwalker, freed her."},
    {"slug": "shadowfall", "name": "Shadowfall Dimension (the dark Kings Canyon)", "kind": "alternate", "parent": "outlands",
     "branch_note": "An alternate Kings Canyon ruled by an alternate Revenant (the Shadow Revenant). The wiki gives no clear divergence point and only suggests his rule may stem from Loba's revenge quest in that world.",
     "description": "A shadowy alternate plane (also called the beta plane) reached by Pathfinder and later by the Legends through Wraith's portals. The scattered pieces of Ash's head were hidden here."},
    {"slug": "alter-multiverse", "name": "Alter's Dying Worlds", "kind": "alternate", "parent": "outlands",
     "branch_note": "Not a single branch: the set of other realities Alter (YingLing Lui) travels through before she reaches the main reality in 2735, several of them destroyed by a version of Horizon.",
     "description": "The many realities Alter visits through the Void, watching worlds end. Here she steals an Ark shard, and a parallel Olympus from these realities later breaks through into the main reality."},
]

entities = []
def E(slug, name, kind, summary, src, aliases=None, timeline=None, variant_of=None):
    entities.append({"slug": slug, "name": name, "kind": kind, "timeline": timeline, "variant_of": variant_of,
                     "aliases": aliases or [], "summary": summary, "sources": src})

def L(s):
    return ["wiki-" + s, "ea-" + s]

# ---- Legends ----
E("bloodhound", "Bloodhound", "character", "A hunter from Talos, orphaned when a flash freeze hit the town of World's Edge and raised by uncle Artur in the Old Ways, a tribe that rejects technology. Coolant scarred their face and lungs when they killed a Goliath. They entered the Apex Games in 2732 to win honor so that their dead lover Boone can reach Valhalla.", L("bloodhound"), ["Blóðhundr"])
E("gibraltar", "Gibraltar", "character", "Makoa Gibraltar, a search-and-rescue operator from Solace and the grandson of Project Iris scientist Aleki Gibraltar. A teenage joyride with his boyfriend Nik ended in a mudslide that cost his father an arm. He joined the Games in 2730 to bring other competitors home alive.", L("gibraltar"), ["Makoa Gibraltar"])
E("lifeline", "Lifeline", "character", "Ajay Che, a combat medic from Olympus and the daughter of the war-profiteering Che family that owns Chevrex. She cut ties with her parents, joined the humanitarian Frontier Corps and entered the Games in 2731 to fund it. Later she worked against Torres Silva and broke Mad Maggie out of prison.", L("lifeline"), ["Ajay Che"])
E("pathfinder", "Pathfinder", "character", "A custom MRVN robot built on February 4, 2658 by the Project Iris scientists to tend their branthium refinery. On December 25, 2658 he triggered the self-destruct that stopped a theft and spread branthium across the Outlands. He woke in 2700 with no memory and joined the Games in 2729 to find his creators.", L("pathfinder"), ["MRVN"])
E("wraith", "Wraith", "character", "Dr. Renee Hope Blasey, born in 2701 on Typhon in a reality where the IMC won the Frontier War. A phase experiment there left her with amnesia and voices in her head. In 2727 an alternate self freed her and she crossed into the main reality, where she became a Legend in 2730 to learn about her past.", L("wraith"), ["Renee Hope Blasey", "Subject 61137"])
E("bangalore", "Bangalore", "character", "Anita Williams, an IMC soldier from Gridiron. Her brother Jackson took their ship, the Hestia-01, away from the losing Battle of Gridiron to the Outlands. She lost him in 2721 and entered the Games in 2730 to pay for a trip home, then learned that he was still alive.", L("bangalore"), ["Anita Williams"])
E("caustic", "Caustic", "character", "Alexander Nox, a chemist from Gaea who tested gases on people at Humbert Labs. In 2723 he killed his superior, burned the lab and faked his own death, and he later took the name Dr. Mikhail Caustic. He entered the Games in 2731 to test his gases on living subjects. Crypto is his adoptive brother.", L("caustic"), ["Alexander Maxwell Nox", "Dr. Mikhail Caustic"])
E("mirage", "Mirage", "character", "Elliott Witt from Solace, son of the hologram engineer Evelyn Witt. His three brothers went missing in the Outlands Civil War. He runs the Paradise Lounge bar and joined the Games in 2732 for fame and money.", L("mirage"), ["Elliott Witt"])
E("octane", "Octane", "character", "Octavio Silva, a daredevil heir from Olympus. He lost both legs in a grenade-powered Gauntlet stunt and replaced them with bionic legs. He later learned that the man he called his father, Eduardo Silva, was really his grandfather Torres.", L("octane"), ["Octavio Silva"])
E("wattson", "Wattson", "character", "Natalie Paquette, daughter of the Games' electrical engineer Luc Paquette and granddaughter of Project Iris geologist Amélie Paquette. As a child she designed the Ring that encloses each arena. When Luc died just before the Games launched, the Legends took her in as family.", L("wattson"), ["Natalie Paquette"])
E("crypto", "Crypto", "character", "Tae Joon Park, a hacker from Gaea adopted by Katerina 'Mystik' Nox. In 2731 he and his foster sister Mila found an algorithm that predicts Apex Games results. He was then framed for her apparent murder. He entered the Games under the name Hyeon Kim to take revenge on the Syndicate.", L("crypto"), ["Tae Joon Park", "Hyeon Kim"])
E("revenant", "Revenant", "character", "Kaleb Cross, a Syndicate assassin killed in 2400 whose mind Hammond Robotics put into a simulacrum body that came online in 2420. In 2708 damage to his programming showed him what he had become. He then hunted his makers, wanted only death, and was later placed in the Games. In 2735 he took back his source code and killed Torres Silva.", L("revenant"), ["Kaleb Cross"])
E("loba", "Loba", "character", "Loba Andrade, a master thief who saw Revenant kill her parents in 2708. She uses a teleportation bracelet built from stolen Hammond jump-drive tech. In 2733 she destroyed a Revenant body factory under Skull Town, entered the Games, and made it her goal to make Revenant suffer.", L("loba"), ["Loba Andrade", "The Wolf of Psamathe"])
E("rampart", "Rampart", "character", "Ramya Parekh, a weapon modder and former Arenas star from Gaea. A gang called The Sisters burned down her shop, and Kuben Blisk then gave her an Apex card. She built Valkyrie's jetpack and later rented space in Mirage's Paradise Lounge.", L("rampart"), ["Ramya Parekh"])
E("horizon", "Horizon", "character", "Dr. Mary Somers, the astrophysicist who discovered branthium. In 2646 her assistant Ashleigh Reid left her stranded at a black hole, and time dilation made her 87 years late to return home. She fights in the Games to fund time travel research so that she can get back to her son Newton.", L("horizon"), ["Dr. Mary Somers"])
E("fuse", "Fuse", "character", "Walter Fitzroy Jr., a gladiator from Salvo and Mad Maggie's childhood friend. When Salvo joined the Syndicate in 2734 he was picked for the Games, and Maggie blew off his arm with their shared grenade. He later began a relationship with Bloodhound and proposed to them.", L("fuse"), ["Walter Fitzroy Jr."])
E("valkyrie", "Valkyrie", "character", "Kairi Imahara from Angelia, daughter of the Apex Predators pilot Viper, who died on Typhon. She salvaged his Northstar Titan, went to confront Kuben Blisk in 2734, and left with an Apex card. Rampart turned the Titan's parts into her jetpack.", L("valkyrie"), ["Kairi Imahara"])
E("seer", "Seer", "character", "Obi Edolasim, born on Boreas in 2708 at the moment a comet struck the moon Cleo, so his people called him a cursed child. He became an Arenas star for outcasts and joined the Games in 2734. His push to bring the Games to Boreas led to the colony of Hope on Cleo becoming an arena.", L("seer"), ["Obi Edolasim"])
E("ash", "Ash", "character", "Dr. Ashleigh Reid, who betrayed Mary Somers and Project Iris and died in the 2658 Phase Runner incident. Her mind was put into a simulacrum body. As an Apex Predator she fought Jack Cooper on Typhon in Titanfall 2. After Horizon broke her ego retention system, her suppressed compassionate side, Leigh, woke up.", L("ash"), ["Dr. Ashleigh Reid", "Leigh (suppressed personality)"])
E("mad-maggie", "Mad Maggie", "character", "Margaret Kōhere, a Salvonian warlord and leader of the Cracked Talon who fought for Salvo's independence from the Syndicate. She blew off Fuse's arm and attacked Kings Canyon. The Syndicate then sentenced her to fight in the Games.", L("mad-maggie"), ["Margaret Kōhere", "Maggie"])
E("newcastle", "Newcastle", "character", "Jackson Williams, Bangalore's older brother. As commander of the IMS Hestia-01 he deserted the Battle of Gridiron. He let everyone believe he died in 2721 and lived in Harris Valley as Lamont Craig. In 2734 he took the armor and name of the town's dead hero Newcastle to pay off a gang.", L("newcastle"), ["Jackson Williams", "Lamont Craig"])
E("vantage", "Vantage", "character", "Xiomara Contreras, a sniper raised alone on the ice world Págos by her mother Xenia, who had escaped the prison ship GDS Vantage. Xenia was arrested again after she called for help to save her daughter. Mara and her bat Echo joined the Games to draw attention to Xenia's case.", L("vantage"), ["Xiomara Contreras", "Mara"])
E("catalyst", "Catalyst", "character", "Tressa Crystal Smith, a trans ferrofluid witch from Boreas who worked as a terraformer for the Cleo Recovery Council in the colony of Hope. When the Syndicate made Hope an arena, she lost her job. She entered the Games to support her found family.", L("catalyst"), ["Tressa Crystal Smith"])
E("ballistic", "Ballistic", "character", "August Montgomery Brinkman, the first celebrity of the old Thunderdome games. His showboating led to the death of his brother-in-law Kit Siang in 2718, and he withdrew from the world. In 2735 he forced the Syndicate to let him compete in place of his son Nathaniel.", L("ballistic"), ["August Montgomery Brinkman"])
E("conduit", "Conduit", "character", "Rowenna Divina from Nexus, a lifelong fan of the Apex Games. She built a combat rig from the radioactive battery of a fallen Monarch Titan to win money for her family, even though its radiation is slowly killing her. She was the first person from Nexus invited to the Games.", L("conduit"), ["Rowenna Valentina Coffey Divina"])
E("alter", "Alter", "character", "YingLing Lui, a trickster who travels between realities with Void technology and likes to watch worlds end. She noticed that a version of Horizon caused many of these endings. In 2735 she reached the main reality and offered Horizon a stolen Ark shard to power her time machine.", L("alter") + ["ea-upheaval-patch-notes"], ["YingLing Lui"])
E("sparrow", "Sparrow", "character", "Enea Davide Guarino, an archery prodigy from the Clessidra Rossa, a respected bounty-hunter clan on Psamathe. A reckless act got him cast out of the clan and his family. He now hunts bounties alone and joined the Games hoping to win back his family's respect.", L("sparrow") + ["wiki-season-25"], ["Enea Davide Guarino"])
E("axle", "Axle", "character", "Isa Wegner, a racer in Salvo's violent Redline motorcycle battle royale, which killed her father. Kuben Blisk offered an Apex Card to that season's champion. She won it in a final race that killed her rival Weaver.", L("axle") + ["wiki-season-29", "ea-overclocked-patch-notes"], ["Isa Wegner"])

# ---- Alternate / variant characters ----
E("voidwalker-wraith", "Voidwalker Wraith", "character", "The main reality's own Renee Blasey, a cruel ARES scientist who gained the power to travel between dimensions through Project Wraith. In 2727 she went looking for revenge on Amer Singh, entered the IMC-victory reality, freed her captive counterpart, and stayed behind to fight Singh. Her fate is unknown.", ["wiki-voidwalker-wraith", "wiki-wraith"], ["Dr. Renee Hope Blasey (main reality)", "the Voidwalker"], None, "wraith")
E("shadow-revenant", "Shadow Revenant", "character", "An alternate Kaleb Cross who became a simulacrum hitman like his main-reality self and now rules the dark alternate Kings Canyon of the Shadowfall dimension. He first resented the Legends' intrusion but helped them recover the last piece of the artifact.", ["wiki-shadow-revenant", "wiki-revenant"], ["Kaleb Cross (Shadowfall)"], "shadowfall", "revenant")
E("amer-singh", "Amer Singh", "character", "An ARES Division scientist and Renee Blasey's partner on Project Wraith. In Wraith's home reality he kept experimenting on her after the test wiped her memory. The Voidwalker stayed behind to fight him. The main reality's Singh was already dead.", ["wiki-amer-singh", "wiki-voidwalker-wraith", "wiki-wraith"], [], "imc-victory")
E("alternate-olympus", "Alternate Olympus", "place", "A parallel version of the floating city of Olympus that appeared and vanished through portals around the Outlands in 2735. One appearance destroyed Cleo's stasis net satellite and devastated the Broken Moon arena.", ["wiki-alter", "wiki-broken-moon", "wiki-olympus"], [], "alter-multiverse", "olympus")

# ---- Supporting characters (canon) ----
sc = [
 ("kuben-blisk", "Kuben Blisk", "Leader of the Apex Predators mercenaries and Titanfall 2 antagonist, who later became commissioner of the Apex Games. He fought in the old Thunderdome from 2704 to 2710. He personally recruits Legends such as Wattson, Rampart, Valkyrie and Axle.", ["wiki-kuben-blisk", "wiki-apex-predators"], ["Commissioner Blisk"]),
 ("torres-silva", "Torres Silva", "Founder of Silva Pharmaceuticals and Octane's grandfather. He stays young with a special strain of Stim. After his son Eduardo died, he took Eduardo's identity. In 2734 he became the Syndicate's sole leader, and Revenant killed him in 2735.", ["wiki-torres-silva", "wiki-octane", "wiki-mercenary-syndicate"], ["Eduardo Silva (assumed identity)"]),
 ("eduardo-silva", "Eduardo Silva", "Torres Silva's son and Octane's real father. Torres made Stim while trying to cure Eduardo's terminal illness. Eduardo died years before the Games, and his father secretly took his name.", ["wiki-torres-silva", "wiki-octane"], []),
 ("jaime", "Jaime", "Loba's partner in crime and friend, whom she once rescued. Instead of disposing of Revenant's source code as she asked, he kept it. In 2734 an unknown attacker took it from him and left him badly hurt.", ["wiki-loba", "wiki-timeline"], []),
 ("mila-alexander", "Mila Alexander", "Crypto's foster sister, who worked Syndicate jobs with him. She was taken in 2731 and presumed dead, but she survived in hiding and works inside the Syndicate to find out who framed her brother.", ["wiki-crypto", "wiki-wattson", "wiki-timeline"], []),
 ("mystik", "Mystik", "Katerina Tikacek Nox, Caustic's mother and Crypto's adoptive mother. She fell ill in the Medusa outbreak and survived. During her recovery she reunited with Caustic, whom she had believed dead.", ["wiki-caustic", "wiki-crypto"], ["Katerina Tikacek Nox"]),
 ("newton-somers", "Newton Somers", "Horizon's son, who interned with Project Iris and helped create Pathfinder while his mother was lost in space. He was officially listed as dead after the 2658 incident, but Leigh tells Horizon that he did not die then.", ["wiki-horizon", "wiki-project-iris", "wiki-ash"], ["Newt"]),
 ("amelie-paquette", "Dr. Amélie Paquette", "The Project Iris geologist and Wattson's grandmother. During the 2658 theft, Reid cut off her hand, and she stabbed Reid with Reid's own sword. She then told Pathfinder to start the self-destruct.", ["wiki-project-iris", "wiki-ash", "wiki-pathfinder"], []),
 ("aleki-gibraltar", "Dr. Aleki Gibraltar", "A Project Iris scientist who first warned of the Outlands energy crisis and helped create Pathfinder. He is Gibraltar's grandfather and died in the 2658 explosion.", ["wiki-project-iris", "wiki-gibraltar"], []),
 ("luc-paquette", "Luc Paquette", "Wattson's father, an electrical engineer hired by the Syndicate to build the power grid for the new Games on Kings Canyon. He took public credit for his daughter's Ring design at her request and died just before the Games began.", ["wiki-wattson", "wiki-timeline"], []),
 ("lillian-peck", "Lillian Peck", "The billionaire philanthropist who paid for Olympus in 2640 and founded Project Iris in 2643 to avert an energy crisis. She cared for Newton while Horizon was away and was a mentor to Horizon.", ["wiki-olympus", "wiki-project-iris", "wiki-horizon"], []),
 ("boone", "Boone", "A hunter of rare creatures who became Bloodhound's lover. He captured the elusive óséður to sell to the Thunderdome on Solace, where it escaped and killed him.", ["wiki-bloodhound"], []),
 ("artur", "Artur", "Bloodhound's uncle, who raised them in the Old Ways and died fighting a Goliath. Bloodhound named their raven companion after him.", ["wiki-bloodhound"], []),
 ("nik-gentile", "Nik Gentile", "Gibraltar's first boyfriend. He took the blame for the mudslide accident and went to juvenile detention. He is the father of Michael Gentile.", ["wiki-gibraltar"], ["Nikolas Gentile"]),
 ("michael-gentile", "Michael Gentile", "Nik's son, who came to resent Gibraltar after learning about his father's past. Gibraltar later saved him from a sinking Trident in Norlock Lake.", ["wiki-gibraltar", "wiki-mirage"], []),
 ("cherisse-che", "Cherisse Che", "Lifeline's mother, a powerful Psamathian with Syndicate ties and a close ally of Torres Silva. Torres put her at the head of the militarized Syndicate Corps.", ["wiki-lifeline", "wiki-torres-silva"], []),
 ("darion-che", "Darion Che", "Lifeline's father and CEO of the arms-and-drones company Chevrex. He gave the Legends an antique MRVN battery after they stopped an attack on his charity event.", ["wiki-lifeline", "wiki-pathfinder"], []),
 ("viper", "Viper", "An Apex Predators Titan pilot and Valkyrie's father. Jack Cooper and BT-7274 killed him while he escorted the Ark during the Battle of Typhon.", ["wiki-valkyrie", "wiki-apex-predators"], []),
 ("jack-cooper", "Jack Cooper", "The Frontier Militia pilot who, with his Titan BT-7274, beat the Apex Predators on Typhon in Titanfall 2. He killed Viper and crushed Ash's simulacrum body.", ["wiki-ash", "wiki-valkyrie", "wiki-frontier-war"], []),
 ("sandringham-kelly", "Sandringham Kelly", "A Salvonian warlord who became Supreme Warlord and signed the 2734 treaty that made Salvo the seventh Syndicate planet.", ["wiki-timeline", "wiki-mad-maggie"], []),
 ("xenia-contreras", "Xenia Contreras", "Vantage's mother, a prisoner who escaped the GDS Vantage. Called a traitor of the Outlands Civil War, she was arrested again after she set off a distress beacon to save her daughter.", ["wiki-vantage", "wiki-timeline"], []),
 ("diwa", "Diwa", "Conduit's oldest sister, whose injury pushed Conduit to fight for money. She strongly opposes Conduit's use of the radioactive battery.", ["wiki-conduit"], []),
 ("nathaniel-phua", "Nathaniel Phua", "Ballistic's son, who qualified for the Apex Games. His father forced his way in instead, and Nathaniel publicly showed his hatred for him.", ["wiki-ballistic", "wiki-timeline"], []),
 ("sok-leng-phua", "Sok Leng Phua", "A Thunderdome fighter, Ballistic's wife and Nathaniel's mother. She left August after her brother Kit Siang's death.", ["wiki-ballistic"], []),
 ("kit-siang-phua", "Kit Siang Phua", "Sok Leng's brother and Ballistic's Thunderdome teammate. He was killed in the arena in 2718 while August played to the crowd.", ["wiki-ballistic", "wiki-timeline"], []),
 ("evelyn-witt", "Evelyn Witt", "Mirage's mother, a hologram engineer who once worked with the IMC. She has dementia. Her old IMC files gave Wraith her birthday.", ["wiki-mirage", "wiki-wraith"], []),
 ("forge", "Forge", "James 'The Forge' McCormick, a Hammond-sponsored fighter announced as the next Legend. Revenant killed him on live television before he could compete.", ["wiki-revenant", "wiki-timeline"], ["James McCormick"]),
 ("quentin-willis", "Quentin 'Boss' Willis", "A Syndicate official who was secretly fixing the Games. He hired Revenant to recover Crypto's briefcase, and Revenant killed him after the scheme came out.", ["wiki-crypto", "wiki-revenant", "wiki-timeline"], ["Boss Willis"]),
 ("creighton-sawtelle", "Creighton Sawtelle", "The leader of terrorists hired by Torres Silva to attack a Chevrex charity event in Malta, Psamathe in 2733.", ["wiki-lifeline", "wiki-torres-silva"], []),
 ("lisa-stone", "Lisa Stone", "An Outlands TV host and Silva Pharmaceuticals mouthpiece. She turned an interview with Seer into an attack on his character and later interviewed Revenant.", ["wiki-seer", "wiki-revenant", "wiki-timeline"], []),
 ("marcos-andrade", "Marcos Andrade", "A celebrated thief and Loba's father. A victim of his theft put a Syndicate bounty on him, and Revenant killed him at Tenmei in 2708.", ["wiki-loba", "wiki-revenant"], []),
 ("alanza-andrade", "Alanza Andrade", "Loba's mother, a professional thief. Revenant killed her at Tenmei in 2708 after she shot at him.", ["wiki-loba", "wiki-revenant"], []),
 ("weaver", "Weaver", "Axle's only real rival in Redline. She died in the final race that won Axle her Apex Card.", ["wiki-axle", "ea-axle"], []),
 ("aurora", "Aurora", "Sparrow's younger sister, whom he had to leave behind when the Clessidra Rossa cast him out.", ["wiki-sparrow"], []),
 ("zeke-williams", "Zeke Williams", "The oldest Williams sibling, killed with the IMC garrison when Typhon was destroyed.", ["wiki-bangalore", "wiki-frontier-war"], []),
 ("scryer", "Commander Scryer", "An IMC cloak pilot who answered Anita's distress call in 2716 and tried to execute Jackson for desertion. The siblings killed him, and Anita kept his data knife.", ["wiki-bangalore", "wiki-newcastle"], []),
 ("franklin-humbert", "Dr. Franklin Humbert", "Head of Humbert Labs. Caustic killed him in 2723 after Humbert discovered his human experiments.", ["wiki-caustic", "wiki-minor-characters"], []),
 ("victor-maldera", "Victor Maldera", "A former Gaean police lieutenant obsessed with the Humbert Labs case. In 2725 he found footage in Pathfinder's memory that proves Nox survived.", ["wiki-caustic", "wiki-pathfinder"], []),
 ("heinrich-hammond", "Dr. Heinrich Hammond", "Founder of Hammond Engineering (2127) and Hammond Robotics (2131). Hammond Engineering grew into the IMC.", ["wiki-imc", "wiki-hammond-robotics", "wiki-timeline"], []),
]
for slug, name, summ, src, al in sc:
    E(slug, name, "character", summ, src, al)

# ---- Factions / organizations ----
orgs = [
 ("mercenary-syndicate", "Mercenary Syndicate", "faction", "A coalition of mercenary companies that rules the seven planets of Syndicate Space and organizes the Apex Games. A council ran it until 2734, when Torres Silva became its single leader.", ["wiki-mercenary-syndicate"], ["The Syndicate", "Syndicate Alliance of Free Worlds"]),
 ("imc", "Interstellar Manufacturing Corporation", "faction", "The megacorporation that grew out of Hammond Engineering and fought the Frontier Militia in the Titan Wars and the Frontier War. It withdrew from its last Outlands planet in 2719.", ["wiki-imc", "wiki-frontier-war"], ["IMC"]),
 ("frontier-militia", "Frontier Militia", "faction", "The Frontier colonists' army that resisted the IMC. In the main reality it won the Frontier War, destroying the Demeter gateway and Typhon's Fold Weapon.", ["wiki-frontier-war", "wiki-imc"], ["The Militia"]),
 ("apex-predators", "Apex Predators", "faction", "The elite mercenary unit of the Mercenary Syndicate, led by Kuben Blisk. Ashleigh Reid led its men at Project Iris in 2658, and it later fought for the IMC on Typhon. The Apex Games are named after it.", ["wiki-apex-predators", "wiki-kuben-blisk"], []),
 ("hammond-robotics", "Hammond Robotics", "organization", "A former IMC subsidiary that makes simulacra and machinery. It built Revenant, put its Planetary Harvester on World's Edge, and partnered with the Syndicate after 2733.", ["wiki-hammond-robotics"], []),
 ("frontier-corps", "Frontier Corps", "organization", "A humanitarian organization founded in 2711 that serves Frontier communities. Lifeline joined it. In 2734 Torres Silva absorbed it and renamed it the militarized Syndicate Corps under Cherisse Che.", ["wiki-lifeline", "wiki-timeline"], ["Syndicate Corps"]),
 ("silva-pharmaceuticals", "Silva Pharmaceuticals", "organization", "The drug company Torres Silva founded around his Stim formula. It secretly sent the Icarus fleet and its Medusa vine cargo to Olympus.", ["wiki-torres-silva", "wiki-olympus"], []),
 ("chevrex", "Chevrex", "organization", "The Che family's company, which makes drones and profits from Frontier wars. It also helped fund Project Iris.", ["wiki-lifeline", "wiki-pathfinder"], ["Chevrex Inc."]),
 ("project-iris", "Project Iris", "organization", "The scientific group, also called the Group, that Lillian Peck founded in 2643 to solve the Outlands energy crisis with branthium. Its scientists built Pathfinder, and most of them died on December 25, 2658.", ["wiki-project-iris"], ["The Group"]),
 ("cracked-talon", "Cracked Talon", "faction", "Mad Maggie's Salvonian warband. It raided Syndicate supply ships and fought for Salvo's independence. Most of its members put down their arms after Salvo prospered under the Syndicate.", ["wiki-mad-maggie"], []),
 ("forgotten-families", "Forgotten Families", "faction", "A gang that tortures and kills IMC deserters. It took over Harris Valley's debts and blackmailed Jackson Williams into the Games.", ["wiki-newcastle", "wiki-mirage"], []),
 ("saras", "Search and Rescue Association of Solace", "organization", "A rescue group founded by the Gibraltar family in 2525. Gibraltar and his parents serve in it.", ["wiki-gibraltar", "wiki-timeline"], ["S.A.R.A.S."]),
 ("ares-division", "ARES Division", "faction", "The IMC's research and archaeology division. It ran the Fold Weapon on Typhon and phase experiments such as Project Wraith.", ["wiki-wraith", "wiki-frontier-war"], []),
 ("cleo-recovery-council", "Cleo Recovery Council", "organization", "The group terraforming Boreas's broken moon Cleo through the colony of Hope. The Syndicate ended its work there when Hope became an Apex arena.", ["wiki-broken-moon", "wiki-catalyst"], ["CRC"]),
 ("clessidra-rossa", "Clessidra Rossa", "organization", "The Outlands' most respected clan of bounty hunters, known for archery and a strict moral code. Sparrow was raised in it and then cast out.", ["wiki-sparrow", "ea-sparrow"], ["Red Hourglass"]),
 ("the-sisters", "The Sisters", "faction", "Big Sister's gang. It burned down Rampart's shop when she refused to throw a match and later became a licensed weapons business.", ["wiki-rampart", "wiki-timeline"], []),
 ("humbert-labs", "Humbert Labs", "organization", "A pesticide-gas maker in Zaldana City, Gaea, where Caustic once worked. In 2735 a crash at one of its sites spread toxic gas through Suotamo's E-District.", ["wiki-caustic", "wiki-e-district"], []),
 ("apex-games", "Apex Games", "organization", "The televised bloodsport the Syndicate created after the Outlands Civil War, revived from the IMC soldiers' Thunderdome and named after the Apex Predators. It began in 2729 under commissioner Kuben Blisk.", ["wiki-apex-games", "wiki-mercenary-syndicate"], ["The Games"]),
]
for slug, name, kind, summ, src, al in orgs:
    E(slug, name, kind, summ, src, al)

# ---- Places ----
places = [
 ("the-outlands", "The Outlands", "A region of the Frontier settled in the 2300s. After the IMC left, it split into Syndicate Space and the independent Fringe Worlds.", ["wiki-timeline", "wiki-mercenary-syndicate"], []),
 ("solace", "Solace", "A Syndicate planet that is home to Solace City, Kings Canyon, Harris Valley and the Paradise Lounge. It was the last Outlands planet the IMC left, in 2719.", ["wiki-timeline", "wiki-kings-canyon"], []),
 ("talos", "Talos", "A volcanic planet rich in branthium and home of the New Dawn plant, World's Edge and Bloodhound's tribe.", ["wiki-worlds-edge", "wiki-bloodhound"], []),
 ("psamathe", "Psamathe", "A wealthy planet with the city of Malta. The floating city of Olympus was built above it.", ["wiki-olympus", "wiki-lifeline"], []),
 ("gaea", "Gaea", "A planet that holds the city of Suotamo, Storm Point and Humbert Labs.", ["wiki-storm-point", "wiki-e-district"], []),
 ("boreas", "Boreas", "A failing planet damaged by its broken moon Cleo. It is Seer's and Catalyst's homeworld.", ["wiki-broken-moon", "wiki-seer"], []),
 ("salvo", "Salvo", "A harsh planet of warlords and the Bonecage arena. It joined Syndicate Space in 2734 as the seventh planet. It is home to Fuse, Mad Maggie and Axle.", ["wiki-mad-maggie", "wiki-mercenary-syndicate"], []),
 ("gridiron", "Gridiron", "The Williams family's IMC homeworld and the site of the Battle of Gridiron. It is about twenty years' travel from the Outlands.", ["wiki-bangalore"], []),
 ("typhon", "Typhon", "The planet of the IMC's Fold Weapon, destroyed in 2715 at the end of Titanfall 2. It was Wraith's birthplace.", ["wiki-frontier-war", "wiki-wraith"], []),
 ("nexus", "Nexus", "A neutral Fringe World. A revolution there overthrew its monarchy, and the sacrifice of a Monarch Titan in that war left a radioactive quarantine zone. It is Conduit's home.", ["wiki-conduit", "wiki-timeline"], []),
 ("pagos", "Págos", "A frozen Fringe World where the prison ship GDS Vantage crashed. Vantage grew up there.", ["wiki-vantage"], []),
 ("kings-canyon", "Kings Canyon", "A former IMC research island on Solace with Singh Labs and the Thunderdome. It became the first Apex Games arena in 2729.", ["wiki-kings-canyon"], []),
 ("worlds-edge", "World's Edge", "A frozen-and-volcanic mining town on Talos around the New Dawn plant. It became the second arena, and Hammond's Planetary Harvester devastated it.", ["wiki-worlds-edge"], []),
 ("olympus", "Olympus", "A floating research city above Psamathe, built in 2640 by Lillian Peck. The 2658 Phase Runner incident left the Rift there. It became an arena in 2733 and later suffered the Medusa outbreak.", ["wiki-olympus"], []),
 ("storm-point", "Storm Point", "A storm-wrapped island on Gaea where the IMS Hestia-01 crashed in 2716. It became an Apex arena in 2734.", ["wiki-storm-point"], []),
 ("broken-moon", "Broken Moon", "The colony of Hope on Boreas's moon Cleo, shattered by a comet in 2708 and terraformed by the CRC. The Syndicate made it an arena in 2734.", ["wiki-broken-moon"], ["Cleo", "Hope"]),
 ("e-district", "E-District", "The Electro District of Suotamo on Gaea. It was evacuated after power riots and Alter's toxic-gas incident, then restored as an arena.", ["wiki-e-district", "ea-shockwave-patch-notes"], ["Electro District"]),
 ("paradise-lounge", "Paradise Lounge", "Mirage's bar in Solace City and the Legends' usual meeting place. Rampart once kept her shop there.", ["wiki-mirage", "wiki-rampart"], []),
 ("singh-labs", "Singh Labs", "The ARES phase-research lab on Kings Canyon where Project Wraith took place and where Wraith crossed between realities.", ["wiki-wraith", "wiki-amer-singh"], []),
 ("harris-valley", "Harris Valley", "A town on Solace founded by people the IMC left behind. Jackson Williams lives there as Lamont Craig.", ["wiki-newcastle", "wiki-bangalore"], []),
 ("thunderdome", "Thunderdome", "The gladiator arena IMC soldiers built on Kings Canyon in 2703, the forerunner of the Apex Games. Blisk and Ballistic both fought there.", ["wiki-kings-canyon", "wiki-ballistic"], []),
 ("the-void", "The Void", "A space between realities used for phasing. Wraith's voices are alternate versions of herself that speak to her through it. Alter's technology also uses it.", ["wiki-void", "wiki-wraith", "wiki-alter"], []),
 ("shadowfall-kings-canyon", "Shadowfall Kings Canyon", "The dark alternate Kings Canyon of the Shadowfall dimension, ruled by the Shadow Revenant. The nine pieces of Ash's head were buried there.", ["wiki-shadow-revenant", "wiki-ash"], ["Beta plane"]),
]
for slug, name, summ, src, al in places:
    tl = "shadowfall" if slug == "shadowfall-kings-canyon" else None
    vo = "kings-canyon" if slug == "shadowfall-kings-canyon" else None
    E(slug, name, "place", summ, src, al, tl, vo)

# ---- Artifacts ----
arts = [
 ("branthium", "Branthium", "An element Mary Somers found in a black hole's accretion disk. Its refinement by Project Iris ended the Outlands energy crisis in 2658.", ["wiki-horizon", "wiki-project-iris"], []),
 ("revenant-source-code", "Revenant's Source Code", "The preserved remains of Kaleb Cross's head and brain, which keep Revenant's mind running. Loba, Jaime, Hammond and Torres Silva all held it before Revenant took it back in 2735.", ["wiki-revenant", "wiki-loba"], ["the Head"]),
 ("the-ark", "The Ark", "An ancient power source that drove the IMC's Fold Weapon on Typhon. An energy source possibly related to it powered the Hestia-01's escape. Alter stole a shard of an Ark.", ["wiki-frontier-war", "wiki-bangalore", "wiki-alter"], ["Ark shard"]),
 ("the-ring", "The Ring", "The shrinking energy barrier that encloses each Apex arena. Wattson designed it, and her father took the credit at her request.", ["wiki-wattson"], ["Modified Containment Ring"]),
 ("time-travel-device", "Time Travel Device", "A time gauntlet from Torres Silva's collection that matched Horizon's own designs. Octane won it in 2735 and gave it to her.", ["wiki-horizon", "wiki-octane"], ["time gauntlet"]),
 ("medusa-vines", "Medusa Vines", "Plants recovered from Typhon (IMC Project: Legacy). The Icarus fleet brought them to Olympus in 2734, where they spread a deadly antigen.", ["wiki-olympus", "wiki-valkyrie"], ["Legacy Antigen"]),
 ("ims-hestia-01", "IMS Hestia-01", "The IMC ship Jackson Williams commanded. It fled the Battle of Gridiron and crashed on Storm Point in 2716. A 2735 storm destroyed its remains.", ["wiki-newcastle", "wiki-storm-point"], []),
 ("doc-drone", "D.O.C.", "Lifeline's medical drone. In 2735 a rift in reality swallowed it, and she lost her hand pulling it back before she rebuilt it.", ["wiki-lifeline", "ea-lifeline"], ["D.O.C. Heal Drone"]),
 ("vipers-northstar", "Viper's Northstar", "Viper's Northstar-class Titan. Valkyrie recovered it from Typhon's wreckage, and Rampart made her jetpack from it.", ["wiki-valkyrie", "ea-valkyrie"], []),
]
for slug, name, summ, src, al in arts:
    E(slug, name, "artifact", summ, src, al)

# ---------------- EVENTS ----------------
events = []
def V(slug, tl, title, summary, date_label, sort_key, era, imp, parts, src):
    events.append({"slug": slug, "timeline": tl, "title": title, "summary": summary, "date_label": date_label,
                   "sort_key": sort_key, "era": era, "importance": imp,
                   "participants": [{"entity": e, "role": r} for e, r in parts], "sources": src})

ERA_C = "Corporate Age"; ERA_F = "Frontier Era"; ERA_W = "Frontier War"; ERA_CW = "Outlands Civil War"; ERA_PRE = "Pre-Games"; ERA_G = "Apex Games"
O = "outlands"
V("hammond-engineering-founded", O, "Hammond Engineering founded", "Heinrich Hammond starts Hammond Engineering, the company that later becomes the IMC. Four years later he founds Hammond Robotics as a subsidiary.", "2127", 2127.0, ERA_C, 2, [("heinrich-hammond", "founder"), ("hammond-robotics", "subject")], ["wiki-timeline", "wiki-imc", "wiki-hammond-robotics"])
V("imc-formed", O, "The IMC is formed", "Over about a century of mergers and buyouts, Hammond Engineering absorbs most other big Core Systems firms and becomes the Interstellar Manufacturing Corporation.", "2192", 2192.0, ERA_C, 3, [("imc", "subject"), ("heinrich-hammond", "founder")], ["wiki-timeline", "wiki-imc"])
V("frontier-discovered", O, "Discovery of the Frontier", "The discovery of the Frontier starts a new space race, and IMC colony ships found the first settlements there.", "2292", 2292.0, ERA_F, 3, [("imc", "colonizer")], ["wiki-timeline"])
V("outlands-colonized", O, "The Outlands are settled", "Colonists find and settle the Outlands. Among them are the ancestors of the Gibraltar family, who arrive on the IMS Nostros.", "2300s", 2300.0, ERA_F, 3, [("the-outlands", "setting")], ["wiki-timeline", "wiki-gibraltar"])
V("kaleb-cross-killed", O, "Death of Kaleb Cross", "Syndicate assassin Kaleb Cross is killed by Bob Woods, whose family Cross had murdered. The Syndicate sends his body to Hammond Robotics. Revenant later tells this story, and he may not be a reliable narrator.", "2400", 2400.0, ERA_F, 4, [("revenant", "victim"), ("mercenary-syndicate", "employer"), ("hammond-robotics", "recipient")], ["wiki-revenant", "wiki-timeline"])
V("revenant-first-boot", O, "Revenant comes online", "Hammond Robotics uploads Cross's mind into a simulacrum body for the first time and ignores warnings about its stability. He then serves the Syndicate as a deathless hitman for centuries.", "2420", 2420.0, ERA_F, 5, [("revenant", "subject"), ("hammond-robotics", "creator"), ("mercenary-syndicate", "employer")], ["wiki-revenant", "wiki-hammond-robotics", "wiki-timeline"])
V("corporate-wars", O, "The Corporate Wars", "The IMC goes to war with rival corporations in the Core Systems and leaves the Frontier on its own for generations.", "2442", 2442.0, ERA_F, 3, [("imc", "belligerent")], ["wiki-imc", "wiki-timeline"])
V("saras-founded", O, "SARAS founded", "The Gibraltar family founds the Search and Rescue Association of Solace.", "2525", 2525.0, ERA_F, 1, [("saras", "subject")], ["wiki-timeline"])
V("olympus-built", O, "Olympus is built", "Billionaire Lillian Peck pays for the floating research city of Olympus above Psamathe.", "2640", 2640.0, ERA_F, 4, [("lillian-peck", "founder"), ("olympus", "subject")], ["wiki-olympus", "wiki-timeline"])
V("project-iris-founded", O, "Project Iris founded", "Warned of a coming energy crisis, Lillian Peck brings together the Outlands' best scientists as Project Iris.", "2643", 2643.0, ERA_F, 3, [("lillian-peck", "founder"), ("project-iris", "subject"), ("aleki-gibraltar", "member")], ["wiki-project-iris", "wiki-timeline"])
V("somers-betrayed", O, "Betrayal at the black hole", "Mary Somers and her assistant Ashleigh Reid fly to a black hole and collect branthium. Reid cuts Somers's tether and leaves her for dead. Somers escapes, but only 246 days pass for her while 87 years pass at home.", "2646", 2646.0, ERA_F, 5, [("horizon", "victim"), ("ash", "betrayer"), ("branthium", "object")], ["wiki-horizon", "wiki-ash", "wiki-timeline", "ea-horizon"])
V("energy-crisis", O, "Outlands energy crisis", "The predicted energy crisis begins. Project Iris works to refine branthium into a usable fuel.", "2655", 2655.0, ERA_F, 3, [("project-iris", "responder"), ("branthium", "solution")], ["wiki-timeline", "wiki-project-iris"])
V("pathfinder-activated", O, "Pathfinder is built", "The Group fits a MRVN with knowledge from each scientist so it can tend the branthium refinery. It switches on as Pathfinder.", "February 4, 2658", 2658.1, ERA_F, 4, [("pathfinder", "subject"), ("project-iris", "creator"), ("newton-somers", "creator"), ("ash", "creator"), ("amelie-paquette", "creator"), ("aleki-gibraltar", "creator")], ["wiki-pathfinder", "wiki-project-iris", "wiki-timeline"])
V("phase-runner-incident", O, "The Event (Phase Runner incident)", "Reid and Apex Predators mercenaries try to send the first branthium batch to Gridiron. Amélie Paquette stabs Reid, and Pathfinder sends the branthium to its intended destinations and blows up the lab. The blast kills most of the Group, opens the Rift on Olympus and ends the energy crisis.", "December 25, 2658", 2658.98, ERA_F, 5, [("ash", "instigator"), ("apex-predators", "instigator"), ("amelie-paquette", "defender"), ("pathfinder", "hero"), ("project-iris", "victim"), ("olympus", "location"), ("branthium", "object")], ["wiki-project-iris", "wiki-ash", "wiki-pathfinder", "wiki-olympus", "wiki-timeline"])
V("ash-becomes-simulacrum", O, "Reid becomes Ash", "The dying Reid agrees to have her mind put into a simulacrum shell. The process splits her personality and suppresses her compassionate side. As Ash, she keeps working with the Apex Predators.", "December 25, 2658", 2658.99, ERA_F, 4, [("ash", "subject"), ("apex-predators", "ally")], ["wiki-ash", "wiki-timeline", "ea-ash"])
V("titan-wars", O, "The Titan Wars", "The IMC returns to the Frontier and claims eminent domain. It fights the Frontier Militia from 2671 to 2692 and wins.", "2671-2692", 2671.0, ERA_W, 3, [("imc", "victor"), ("frontier-militia", "belligerent")], ["wiki-imc", "wiki-frontier-war", "wiki-timeline"])
V("pathfinder-wakes", O, "Pathfinder awakens", "Pathfinder wakes in an abandoned warehouse on Solace with no memory of his creators. He works a string of odd jobs and is fired from most of them.", "2700", 2700.0, ERA_W, 3, [("pathfinder", "subject"), ("solace", "location")], ["wiki-pathfinder", "wiki-timeline", "ea-pathfinder"])
V("worlds-edge-flash-freeze", O, "Flash freeze at World's Edge", "An accident at the New Dawn coolant plant buries World's Edge in ice and kills Bloodhound's parents. Their uncle Artur takes them in.", "c. 2703", 2703.5, ERA_W, 3, [("bloodhound", "survivor"), ("artur", "guardian"), ("worlds-edge", "location")], ["wiki-bloodhound", "wiki-worlds-edge", "wiki-timeline"])
V("thunderdome-built", O, "The Thunderdome opens", "IMC soldiers on Kings Canyon build the Thunderdome for gladiator fights. Kuben Blisk fights there from 2704 to 2710.", "2703", 2703.0, ERA_W, 2, [("thunderdome", "subject"), ("kuben-blisk", "competitor"), ("kings-canyon", "location")], ["wiki-kings-canyon", "wiki-kuben-blisk", "wiki-timeline"])
V("frontier-war-begins", O, "The Frontier War begins", "With new intelligence on the IMC, the rebuilt Frontier Militia attacks again, starting the war shown in the Titanfall games. August Brinkman starts fighting in the Thunderdome the same year.", "2707", 2707.0, ERA_W, 4, [("frontier-militia", "instigator"), ("imc", "belligerent"), ("ballistic", "witness")], ["wiki-frontier-war", "wiki-timeline"])
V("cleo-comet-strike", O, "Comet shatters Cleo", "A comet hits Boreas's moon Cleo at the moment Obi Edolasim is born, and Boreans brand him a cursed child. The damage threatens Boreas itself.", "2708", 2708.2, ERA_W, 3, [("seer", "born"), ("broken-moon", "location"), ("boreas", "affected")], ["wiki-seer", "wiki-broken-moon", "ea-seer"])
V("tenmei-massacre", O, "The Tenmei massacre", "On a Syndicate contract, Revenant kills Marcos and Alanza Andrade at the Tenmei restaurant on Olympus. A glass shard breaks his ego retention system, and he sees himself as a machine for the first time. Young Loba and Pathfinder, a sous chef there, witness it.", "2708", 2708.5, ERA_W, 5, [("revenant", "instigator"), ("marcos-andrade", "victim"), ("alanza-andrade", "victim"), ("loba", "witness"), ("pathfinder", "witness"), ("mercenary-syndicate", "employer")], ["wiki-revenant", "wiki-loba", "wiki-pathfinder", "wiki-timeline"])
V("battle-of-demeter", O, "Battle of Demeter (Titanfall)", "The Militia destroys the IMC refueling gateway at Demeter and cuts off IMC forces in the Frontier from the Core Systems. Blisk survives the battle.", "2710", 2710.0, ERA_W, 4, [("frontier-militia", "victor"), ("imc", "defeated"), ("kuben-blisk", "combatant")], ["wiki-frontier-war", "wiki-kuben-blisk", "wiki-timeline"])
V("bloodhound-goliath", O, "Bloodhound slays the Goliath", "After a Goliath kills uncle Artur, Bloodhound kills it by freezing it with coolant. The coolant scars their face and lungs, and they later lead the tribe.", "2710", 2710.5, ERA_W, 3, [("bloodhound", "hero"), ("artur", "victim")], ["wiki-bloodhound", "wiki-timeline"])
V("boone-death", O, "Death of Boone", "Bloodhound's lover Boone captures the óséður to sell to the Thunderdome on Solace. The beast escapes and kills him. Bloodhound vows to win honor in his place.", "2713", 2713.0, ERA_W, 3, [("boone", "victim"), ("bloodhound", "witness"), ("thunderdome", "location")], ["wiki-bloodhound", "wiki-timeline", "ea-bloodhound"])
V("valkyrie-steals-northstar", O, "Kairi steals the Northstar", "Young Kairi Imahara takes her father Viper's Northstar Titan for a joyride and is shot down. Viper saves her, then leaves for Typhon.", "2715", 2715.05, ERA_W, 2, [("valkyrie", "instigator"), ("viper", "rescuer"), ("vipers-northstar", "object")], ["wiki-valkyrie", "ea-valkyrie"])
V("battle-of-typhon", O, "Battle of Typhon (Titanfall 2)", "The Militia destroys the IMC's Ark-powered Fold Weapon, and with it the planet Typhon. Jack Cooper and BT-7274 kill Apex Predators including Viper and crush Ash's body. Zeke Williams dies with the IMC garrison.", "2715", 2715.2, ERA_W, 5, [("jack-cooper", "hero"), ("frontier-militia", "victor"), ("imc", "defeated"), ("apex-predators", "defeated"), ("kuben-blisk", "survivor"), ("ash", "defeated"), ("viper", "victim"), ("zeke-williams", "victim"), ("typhon", "location"), ("the-ark", "object"), ("ares-division", "belligerent")], ["wiki-frontier-war", "wiki-ash", "wiki-kuben-blisk", "wiki-valkyrie", "wiki-timeline"])
V("battle-of-gridiron", O, "Battle of Gridiron and the Hestia's flight", "As the Militia surrounds Gridiron, Jackson Williams decides the battle is lost. He sedates his sister Anita and takes the IMS Hestia-01 to the Outlands, using an Ark-like energy source to cross in under a year.", "2715", 2715.5, ERA_W, 4, [("newcastle", "instigator"), ("bangalore", "witness"), ("ims-hestia-01", "vessel"), ("gridiron", "location"), ("frontier-militia", "belligerent")], ["wiki-bangalore", "wiki-newcastle", "wiki-timeline", "ea-bangalore"])
V("hestia-crash", O, "Hestia-01 crash and Scryer's attack", "The Hestia-01 crash-lands on Storm Point. Anita wakes and sends an SOS, which brings IMC Commander Scryer to execute Jackson. The siblings kill him and take his ship as the Hestia-02.", "2716", 2716.0, ERA_CW, 3, [("bangalore", "ally"), ("newcastle", "ally"), ("scryer", "victim"), ("storm-point", "location"), ("ims-hestia-01", "vessel")], ["wiki-bangalore", "wiki-newcastle", "wiki-storm-point", "wiki-timeline"])
V("outlands-civil-war", O, "Outlands Civil War begins", "With the IMC gone, Outlands planets start fighting each other over the power vacuum.", "2716", 2716.2, ERA_CW, 4, [("the-outlands", "setting")], ["wiki-timeline", "wiki-gibraltar"])
V("gibraltar-mudslide", O, "The mudslide in the Cascade Mountains", "Gibraltar and Nik steal his father's motorcycle to enlist in the war and crash in a storm. During the rescue, his father loses an arm, and Nik takes the blame and goes to juvenile detention.", "2717", 2717.0, ERA_CW, 3, [("gibraltar", "instigator"), ("nik-gentile", "victim"), ("saras", "rescuer")], ["wiki-gibraltar", "wiki-timeline", "ea-gibraltar"])
V("nexus-monarch-sacrifice", O, "The Monarch's sacrifice on Nexus", "In the war that ends Nexus's monarchy, a Monarch-class Titan detonates its battery to protect young Rowenna Divina's community. The blast leaves a radioactive quarantine zone.", "2717", 2717.5, ERA_CW, 2, [("conduit", "witness"), ("nexus", "location")], ["wiki-conduit", "wiki-timeline"])
V("kit-siang-death", O, "Kit Siang dies in the Thunderdome", "While Brinkman plays to the crowd, his teammate and brother-in-law Kit Siang is killed. Brinkman's guilt drives him into seclusion and breaks up his family.", "2718", 2718.0, ERA_CW, 2, [("ballistic", "instigator"), ("kit-siang-phua", "victim"), ("sok-leng-phua", "witness")], ["wiki-ballistic", "wiki-timeline", "ea-ballistic"])
V("imc-leaves-outlands", O, "IMC leaves Solace", "The IMC leaves Solace, its last Outlands planet, and the Thunderdome closes. The same year the transport Crimson goes down over Gaea with Mirage's three brothers aboard.", "2719", 2719.0, ERA_CW, 4, [("imc", "withdrawing"), ("solace", "location"), ("mirage", "witness")], ["wiki-timeline", "wiki-mirage", "wiki-hammond-robotics"])
V("margo-bombing", O, "Margo's bombing on Boreas", "Tressa Smith and her friend Margo break into a facility that launches mining equipment to Cleo, and Margo sets off a bomb. Tressa flees and joins the Cleo Recovery Council.", "2719", 2719.5, ERA_CW, 2, [("catalyst", "witness"), ("cleo-recovery-council", "refuge"), ("hammond-robotics", "target")], ["wiki-catalyst", "wiki-timeline"])
V("jackson-lost", O, "Jackson lost over Solace", "A week after Jackson tells Anita about the IMC's planet-killing plans, a grenade blows open the Hestia-02's hull above Solace. Jackson shields Anita and is lost, and he chooses to let her think he is dead.", "2721", 2721.0, ERA_CW, 4, [("newcastle", "victim"), ("bangalore", "witness")], ["wiki-bangalore", "wiki-newcastle", "wiki-timeline", "ea-newcastle"])
V("syndicate-treaty", O, "Civil War ends: Mercenary Syndicate Treaty", "The Outlands Civil War ends. Planets that sign the treaty become Syndicate Space, and the rest become the Fringe Worlds. The treaty also plans to revive the Thunderdome on Kings Canyon, and Luc Paquette is hired to build its power grid.", "2723", 2723.0, ERA_CW, 5, [("mercenary-syndicate", "founder"), ("luc-paquette", "contractor"), ("kings-canyon", "location"), ("apex-games", "subject")], ["wiki-timeline", "wiki-mercenary-syndicate", "wiki-apex-games"])
V("humbert-labs-murder", O, "Murder at Humbert Labs", "Franklin Humbert discovers Alexander Nox's human gas tests. Nox kills him, burns the lab and fakes his own death. Pathfinder, working as a window washer, sees it all.", "2723", 2723.5, ERA_PRE, 3, [("caustic", "instigator"), ("franklin-humbert", "victim"), ("pathfinder", "witness"), ("humbert-labs", "location")], ["wiki-caustic", "wiki-pathfinder", "wiki-timeline", "ea-caustic"])
V("crypto-adopted", O, "Mystik adopts Tae Joon", "Grieving the apparent death of her son Alexander, Katerina 'Mystik' Nox adopts the orphan Tae Joon Park and his foster sister Mila.", "2723", 2723.6, ERA_PRE, 2, [("mystik", "parent"), ("crypto", "adoptee"), ("mila-alexander", "adoptee")], ["wiki-crypto", "wiki-timeline"])
V("fight-night", O, "Fight Night in Malta", "Pathfinder and ex-lieutenant Victor Maldera escape mobsters on Psamathe. Pathfinder's memory reveals footage proving Nox survived and a message from Dr. Amélie, and he gains his grappling hook.", "2725", 2725.0, ERA_PRE, 2, [("pathfinder", "subject"), ("victor-maldera", "ally"), ("caustic", "suspect")], ["wiki-pathfinder", "wiki-caustic", "wiki-timeline"])
V("seer-first-arenas", O, "Seer discovers the Arenas", "Obi Edolasim stumbles into a warehouse Arenas match and finds his calling, becoming a star for outcasts.", "June 2725", 2725.5, ERA_PRE, 2, [("seer", "subject")], ["wiki-seer", "wiki-timeline"])
V("chenosky-heist", O, "Chenosky Auction House heist", "Loba and Jaime steal gems for The Widow. Loba also takes her mother's antique fan, which the owner had set out as bait.", "April 9, 2726", 2726.3, ERA_PRE, 1, [("loba", "instigator"), ("jaime", "ally"), ("alanza-andrade", "memory")], ["wiki-loba", "wiki-timeline"])
V("jackson-weds", O, "Jackson's new life in Harris Valley", "Living as Lamont Craig in Harris Valley, Jackson marries and records a wedding-night video for his parents on Gridiron.", "2727", 2727.1, ERA_PRE, 2, [("newcastle", "subject"), ("harris-valley", "location")], ["wiki-newcastle", "wiki-timeline"])
V("wraith-crosses-over", O, "Wraith arrives in the main reality", "Freed by the Voidwalker, Renee Blasey comes out of the Void into this reality's abandoned Singh Labs. The Apex Games are being built on Kings Canyon above. She learns that the voices she hears are her alternate selves.", "2727", 2727.31, ERA_PRE, 5, [("wraith", "subject"), ("voidwalker-wraith", "rescuer"), ("singh-labs", "location"), ("the-void", "passage")], ["wiki-wraith", "wiki-voidwalker-wraith", "wiki-timeline", "ea-wraith"])
V("anita-singh-labs-drive", O, "The drive at Singh Labs", "Acting on a tip from informant Tae Joon Park, Anita plays a drive at Singh Labs that shows Jackson alive. The Voidwalker Wraith takes the drive before the message ends.", "2727", 2727.32, ERA_PRE, 2, [("bangalore", "victim"), ("crypto", "informant"), ("voidwalker-wraith", "thief"), ("singh-labs", "location")], ["wiki-bangalore", "wiki-crypto", "wiki-wraith", "wiki-timeline"])
V("wattson-ring-test", O, "Wattson's Ring test and her 'ghost'", "Young Natalie Paquette tests her Ring prototype in a storm. Lightning sets the forest on fire, and the newly arrived Wraith carries her to safety. The burned area becomes the Shattered Forest.", "2727", 2727.5, ERA_PRE, 4, [("wattson", "inventor"), ("wraith", "rescuer"), ("luc-paquette", "parent"), ("the-ring", "object"), ("kings-canyon", "location")], ["wiki-wattson", "wiki-wraith", "wiki-timeline", "ea-wattson"])
V("apex-games-begin", O, "The Apex Games begin", "The Syndicate's new bloodsport opens on Kings Canyon, run by commissioner Kuben Blisk and named after the Apex Predators. Luc Paquette dies a month before the launch, and the Legends adopt Wattson as family. Pathfinder enters on Mirage's advice.", "2729", 2729.0, ERA_G, 5, [("apex-games", "subject"), ("mercenary-syndicate", "organizer"), ("kuben-blisk", "commissioner"), ("luc-paquette", "victim"), ("wattson", "mourner"), ("pathfinder", "competitor"), ("mirage", "advisor"), ("kings-canyon", "location")], ["wiki-timeline", "wiki-apex-games", "wiki-wattson", "wiki-pathfinder"])
V("family-business", O, "Family Business heist", "Lifeline and Octane rob a Silva Pharmaceuticals compound for Frontier Corps medicine. Cherisse Che and 'Eduardo' Silva threaten the field hospital until Octane livestreams the standoff.", "c. 2729-2730", 2729.8, ERA_G, 2, [("lifeline", "instigator"), ("octane", "ally"), ("cherisse-che", "antagonist"), ("torres-silva", "antagonist"), ("frontier-corps", "beneficiary")], ["wiki-lifeline", "wiki-octane", "wiki-torres-silva", "wiki-timeline"])
V("early-legends-join", O, "Wraith, Gibraltar and Bangalore join", "Renee Blasey, Makoa Gibraltar and Anita Williams enter the Apex Games. Wraith wants her past, Gibraltar wants to protect others, and Bangalore wants passage home.", "2730", 2730.0, ERA_G, 3, [("wraith", "competitor"), ("gibraltar", "competitor"), ("bangalore", "competitor")], ["wiki-timeline", "wiki-wraith", "wiki-gibraltar", "wiki-bangalore"])
V("crypto-framed", O, "Crypto is framed", "While working on the Games' broadcast system, Tae Joon and Mila find a match-prediction algorithm. The next day Mila vanishes and Tae Joon is framed for her murder, so he goes into hiding.", "November 25, 2731", 2731.9, ERA_G, 4, [("crypto", "victim"), ("mila-alexander", "victim"), ("mercenary-syndicate", "instigator")], ["wiki-crypto", "wiki-timeline", "ea-crypto"])
V("caustic-lifeline-join", O, "Caustic and Lifeline enter the Games", "Ajay Che joins to fund the Frontier Corps, and Alexander Nox joins under his new identity, Dr. Mikhail Caustic, to test his gases. Fuse becomes the oldest Bonecage qualifier the same year.", "2731", 2731.3, ERA_G, 2, [("lifeline", "competitor"), ("caustic", "competitor"), ("fuse", "competitor")], ["wiki-timeline", "wiki-lifeline", "wiki-caustic"])
V("valkyrie-typhon-salvage", O, "Valkyrie salvages Viper's Northstar", "Blisk hires Kairi to recover her father's Northstar from Typhon's wreckage, where she sees the IMC's Medusa vines. She and her mother then move to Gaea.", "2731", 2731.5, ERA_G, 2, [("valkyrie", "smuggler"), ("kuben-blisk", "employer"), ("vipers-northstar", "object"), ("medusa-vines", "discovery")], ["wiki-valkyrie", "wiki-timeline"])
V("bloodhound-mirage-join", O, "Bloodhound and Mirage join", "Bloodhound enters to collect honor for Boone, and Elliott Witt enters for fame and fortune.", "2732", 2732.0, ERA_G, 2, [("bloodhound", "competitor"), ("mirage", "competitor")], ["wiki-timeline", "wiki-bloodhound", "wiki-mirage"])
V("repulsor-emp", O, "Crypto's Repulsor attack (Season 2)", "Crypto sets off an EMP in Kings Canyon's Repulsor tower. Leviathans and flyers overrun the island, and Singh Labs is dug up, where Wraith learns her name.", "Season 2 (2733)", 2733.1, ERA_G, 4, [("crypto", "instigator"), ("kings-canyon", "location"), ("wraith", "beneficiary")], ["wiki-timeline", "wiki-crypto", "wiki-kings-canyon", "wiki-wraith"])
V("crypto-mirage-first-squad", O, "Crypto meets Mirage (Season 3)", "The games move to World's Edge. Crypto, competing as Hyeon Kim, is put in a squad with Mirage, and their 'kid' and 'old man' rivalry begins.", "Season 3 (2733)", 2733.2, ERA_G, 2, [("crypto", "competitor"), ("mirage", "competitor"), ("worlds-edge", "location")], ["wiki-timeline", "wiki-mirage", "wiki-crypto"])
V("forge-murdered", O, "Forge murdered on live TV (Season 4)", "Revenant kills Hammond-sponsored newcomer Forge during a broadcast interview. Syndicate leaders then put Revenant into the Games to contain him.", "Season 4 (2733)", 2733.3, ERA_G, 4, [("revenant", "instigator"), ("forge", "victim"), ("hammond-robotics", "sponsor"), ("mercenary-syndicate", "organizer")], ["wiki-revenant", "wiki-timeline"])
V("skull-town-collapse", O, "Loba sinks Skull Town (Season 5)", "Hunting Revenant, Loba destroys a hidden factory of his bodies under Skull Town, and the town and Thunderdome sink into the river. Hammond's legal head then announces her as a Legend over Bangalore's objection.", "Season 5 (2733)", 2733.4, ERA_G, 4, [("loba", "instigator"), ("revenant", "target"), ("bangalore", "witness"), ("hammond-robotics", "sponsor"), ("kings-canyon", "location")], ["wiki-loba", "wiki-revenant", "wiki-kings-canyon", "ea-loba"])
V("broken-ghost-quest", O, "The Broken Ghost quest", "Loba blackmails the Legends into recovering nine artifact pieces from the Shadowfall dimension for Hammond. Caustic leaks plans to Revenant to keep Wattson and Crypto apart and frames Crypto, which breaks the group's trust. Afterward Revenant tells Loba he wants to die.", "Season 5 (2733)", 2733.45, ERA_G, 4, [("loba", "instigator"), ("caustic", "mole"), ("crypto", "framed"), ("wattson", "victim"), ("revenant", "antagonist"), ("wraith", "portal-keeper"), ("octane", "participant"), ("bangalore", "investigator"), ("gibraltar", "mediator")], ["wiki-loba", "wiki-caustic", "wiki-crypto", "wiki-revenant", "wiki-timeline"])
V("ash-reactivated", O, "Ash reactivated", "The completed artifact turns out to be Ash's head. Mirage puts it on her body in an IMC vault, and she wakes and says 'Welcome to Olympus,' which starts the Games' move to Olympus.", "Season 5 (2733)", 2733.5, ERA_G, 4, [("ash", "subject"), ("mirage", "catalyst"), ("loba", "instigator")], ["wiki-ash", "wiki-timeline"])
V("rampart-shop-burned", O, "Rampart's shop burned (Season 6)", "Big Sister's gang burns down Rampart Mods. Kuben Blisk, who had been off the grid watching her for a year, gives her an Apex card.", "Season 6 (2733)", 2733.55, ERA_G, 3, [("rampart", "victim"), ("the-sisters", "instigator"), ("kuben-blisk", "sponsor")], ["wiki-rampart", "wiki-kuben-blisk", "wiki-timeline", "ea-rampart"])
V("the-first-ship", O, "The First Ship", "Pathfinder finds a memory-wiped Ash in a dumpster and calls her his girlfriend until Blisk collects her. Rampart moves her shop into the Paradise Lounge. Mirage then loads her belongings onto the rocket to Olympus.", "Season 6 (2733)", 2733.58, ERA_G, 2, [("pathfinder", "host"), ("ash", "guest"), ("rampart", "tenant"), ("mirage", "landlord"), ("wraith", "mediator"), ("kuben-blisk", "ally")], ["wiki-ash", "wiki-rampart", "wiki-mirage", "wiki-pathfinder"])
V("overtime", O, "Overtime: Boss Willis falls", "Revenant, hired by Syndicate official Quentin Willis, chases Crypto and Mirage for an encrypted comm unit that connects to Mila. Willis's ship crashes into a Solace City hospital, and Revenant kills him.", "2733", 2733.6, ERA_G, 3, [("crypto", "target"), ("mirage", "ally"), ("wraith", "ally"), ("revenant", "contractor"), ("quentin-willis", "victim"), ("mila-alexander", "contact")], ["wiki-crypto", "wiki-revenant", "wiki-mirage", "wiki-timeline"])
V("olympus-arena-opens", O, "Olympus becomes an arena (Season 7)", "The Games move to the restored floating city. Horizon returns and joins the Games to fund her time travel research.", "Season 7 (2733)", 2733.7, ERA_G, 3, [("olympus", "location"), ("horizon", "competitor"), ("hammond-robotics", "sponsor")], ["wiki-olympus", "wiki-horizon", "wiki-timeline", "ea-horizon"])
V("family-portrait", O, "Family Portrait: the Chevrex gala attack", "Pathfinder, Gibraltar, Lifeline and Octane stop Creighton Sawtelle's terrorist attack on a Chevrex charity event. Octane learns that his 'father' arranged it, and D.O.C. records his confession.", "Season 7 (2733)", 2733.75, ERA_G, 3, [("octane", "witness"), ("lifeline", "ally"), ("gibraltar", "ally"), ("pathfinder", "ally"), ("creighton-sawtelle", "attacker"), ("torres-silva", "instigator"), ("darion-che", "host")], ["wiki-octane", "wiki-lifeline", "wiki-torres-silva", "wiki-timeline"])
V("crypto-reveals-to-wattson", O, "Crypto reveals himself to Wattson", "At World's Edge, Crypto tells Wattson his real name and why he is hiding. The two make up, and she agrees to keep his secret.", "Season 7 (2733)", 2733.78, ERA_G, 2, [("crypto", "subject"), ("wattson", "confidant")], ["wiki-crypto", "wiki-wattson", "wiki-timeline"])
V("loba-hides-source-code", O, "Loba keeps Revenant alive", "Loba finds Revenant's source code and tells him she sent it away so he must keep suffering. He swears to destroy whatever she loves. Jaime, who was meant to dispose of it, secretly keeps it.", "November 2733", 2733.85, ERA_G, 3, [("loba", "instigator"), ("revenant", "victim"), ("jaime", "keeper"), ("revenant-source-code", "object")], ["wiki-loba", "wiki-revenant", "wiki-timeline", "ea-revenant"])
V("pathfinders-quest", O, "Pathfinder's Quest", "Pathfinder interviews the Legends about his origins. Revenant tricks him into believing he killed his creators, and Rampart helps him see through it. Blisk then gives him the truth about Project Iris and mentions a second MRVN built from his spare parts.", "Season 7 (2733)", 2733.9, ERA_G, 3, [("pathfinder", "investigator"), ("kuben-blisk", "informant"), ("revenant", "deceiver"), ("rampart", "ally"), ("horizon", "informant")], ["wiki-pathfinder", "wiki-timeline", "ea-pathfinder"])
V("salvo-joins-fuse-arm", O, "Salvo joins; Maggie takes Fuse's arm (Season 8)", "Sandringham Kelly signs Salvo into Syndicate Space as its seventh planet, and Fuse is picked for the Games. Furious, Maggie throws their shared golden grenade and blows off his arm.", "2734", 2734.05, ERA_G, 4, [("fuse", "victim"), ("mad-maggie", "instigator"), ("sandringham-kelly", "signatory"), ("salvo", "location"), ("mercenary-syndicate", "annexer")], ["wiki-fuse", "wiki-mad-maggie", "wiki-timeline", "ea-mad-maggie"])
V("kings-canyon-attack", O, "Maggie attacks Kings Canyon", "At Fuse's welcome ceremony, Maggie hijacks the IMS Thermopylae's guns and sets off explosives across Kings Canyon. She later takes control of the Ring. After a final fight with Fuse, she falls from a rooftop and is presumed dead.", "Season 8 (2734)", 2734.1, ERA_G, 4, [("mad-maggie", "instigator"), ("fuse", "target"), ("bloodhound", "ally"), ("lifeline", "ally"), ("kings-canyon", "location")], ["wiki-mad-maggie", "wiki-fuse", "wiki-kings-canyon", "wiki-timeline"])
V("caustic-treatment", O, "Caustic Treatment plot foiled", "Caustic turns Kings Canyon's water treatment plant into a lab to gas Solace City. Wattson stops him and keeps quiet only if he tries to become a better man.", "Season 8 (2734)", 2734.12, ERA_G, 3, [("caustic", "instigator"), ("wattson", "hero")], ["wiki-caustic", "wiki-wattson", "wiki-timeline"])
V("legacy-antigen", O, "The Legacy Antigen outbreak (Season 9)", "During Pathfinder's hero dedication on Olympus, the Silva-sent Icarus fleet docks carrying Typhon's Medusa vines and starts a deadly epidemic. Legends hunt Carthage spiders on Gaea for a cure, and Lifeline exposes Torres's role.", "April 2734", 2734.3, ERA_G, 5, [("medusa-vines", "cause"), ("torres-silva", "instigator"), ("silva-pharmaceuticals", "instigator"), ("pathfinder", "honoree"), ("horizon", "researcher"), ("caustic", "advisor"), ("crypto", "ally"), ("bangalore", "victim"), ("mystik", "victim"), ("lifeline", "investigator"), ("octane", "accomplice"), ("olympus", "location")], ["wiki-olympus", "wiki-torres-silva", "wiki-lifeline", "wiki-caustic", "wiki-timeline"])
V("loba-bangalore-just-friends", O, "'Just friends'", "Loba brings Bangalore flowers in hospital and overhears her call them just friends. Valkyrie comforts Loba while Revenant watches and considers which of them to kill.", "Season 9 (2734)", 2734.32, ERA_G, 2, [("loba", "subject"), ("bangalore", "subject"), ("valkyrie", "comforter"), ("revenant", "watcher")], ["wiki-loba", "wiki-bangalore", "wiki-revenant", "wiki-valkyrie"])
V("wraith-bangalore-pact", O, "Wraith and Bangalore's pact", "During the outbreak, Bangalore says she blames Wraith for losing Jackson's message. Wraith explains that the Voidwalker took it, and the two agree to help each other find the truth.", "Season 9 (2734)", 2734.33, ERA_G, 3, [("wraith", "ally"), ("bangalore", "ally"), ("voidwalker-wraith", "subject")], ["wiki-wraith", "wiki-bangalore"])
V("harvester-collapse", O, "World's Edge collapses (Season 10)", "Hammond's Harvester pushes Talos to breaking point, and Hammond adds the Lava Siphon and Climatizer, which do little. Bloodhound faces visions of their guilt and comes out with their confidence restored.", "Season 10 (2734)", 2734.35, ERA_G, 3, [("hammond-robotics", "instigator"), ("worlds-edge", "location"), ("bloodhound", "subject"), ("fuse", "supporter")], ["wiki-worlds-edge", "wiki-bloodhound", "wiki-timeline"])
V("seer-joins", O, "Seer joins the Games", "Arenas star Obi Edolasim is chosen as the newest Legend and wins his last Arenas match with his parents cheering.", "2734", 2734.36, ERA_G, 2, [("seer", "competitor")], ["wiki-seer", "wiki-timeline", "ea-seer"])
V("valkyrie-confronts-blisk", O, "Valkyrie confronts Blisk", "Kairi meets Blisk intending to kill him for her father's death. He talks her down and hands her an Apex card. She shoots the glass from his hand and takes the callsign Valkyrie.", "2734", 2734.37, ERA_G, 3, [("valkyrie", "instigator"), ("kuben-blisk", "target"), ("viper", "memory")], ["wiki-valkyrie", "ea-valkyrie"])
V("ash-awakened", O, "Horizon awakens Leigh", "Believing Ash holds Lillian Peck's mind, Horizon reads jailbreak codes from Crypto to her. Revenant cracks Ash's faceplate to 'free' her, but the codes reveal that Ash is Reid. The suppressed Leigh briefly surfaces and says she knows what happened to Newton.", "Season 10 (2734)", 2734.4, ERA_G, 5, [("horizon", "instigator"), ("ash", "subject"), ("crypto", "supplier"), ("revenant", "attacker"), ("newton-somers", "subject")], ["wiki-ash", "wiki-horizon", "wiki-revenant", "wiki-timeline", "ea-ash"])
V("storm-point-arena", O, "Storm Point arena; Ash joins (Season 11)", "The Syndicate acquires Storm Point. Ash enters the Games to prove she has left her humanity behind and starts working with Crypto. A Syndicate dogfight downs a Cracked Talon fighter over Olympus and Storm Point.", "Season 11 (2734)", 2734.45, ERA_G, 3, [("storm-point", "location"), ("ash", "competitor"), ("crypto", "ally"), ("cracked-talon", "belligerent")], ["wiki-storm-point", "wiki-ash", "wiki-timeline"])
V("ash-attacks-wattson", O, "Ash hunts the Paquette bloodline", "Ash finds and breaks the sword that killed her human body. Seeing Natalie Paquette listed as next of kin, she knocks Wattson into a ravine at Storm Point's Lightning Rod and vows to finish the bloodline.", "Season 11 (2734)", 2734.47, ERA_G, 3, [("ash", "instigator"), ("wattson", "victim"), ("horizon", "witness"), ("amelie-paquette", "memory")], ["wiki-ash", "wiki-wattson", "wiki-horizon"])
V("maggie-sentenced", O, "Maggie sentenced to the Games (Season 12)", "Captured on Olympus and tried for sedition, Maggie is spared from a firing squad when 'Eduardo' Silva steps in. She is sentenced to compete, so the Legends become her executioners.", "Season 12 (2734)", 2734.5, ERA_G, 4, [("mad-maggie", "defendant"), ("torres-silva", "manipulator"), ("mercenary-syndicate", "judge")], ["wiki-mad-maggie", "wiki-torres-silva", "wiki-timeline"])
V("olympus-phase-drop", O, "Olympus dropped over Malta", "During Maggie's first match, Silva hijacks the new Phase Driver and moves Olympus over Malta, then blames Maggie. She proves her innocence to Lifeline and Octane with his stolen glasses.", "Season 12 (2734)", 2734.52, ERA_G, 3, [("torres-silva", "instigator"), ("mad-maggie", "framed"), ("lifeline", "ally"), ("octane", "ally"), ("olympus", "location")], ["wiki-olympus", "wiki-mad-maggie", "wiki-lifeline", "wiki-timeline"])
V("torres-revealed", O, "Torres revealed; Silva becomes One Voice", "Lifeline finds the real Eduardo Silva's death certificate. Octane destroys it and ends their friendship. Torres, still posing as Eduardo, is elected sole leader of the Syndicate, turns the Frontier Corps into the Syndicate Corps under Cherisse Che, and tells Octane he is his grandfather.", "Season 12 (2734)", 2734.55, ERA_G, 5, [("torres-silva", "instigator"), ("octane", "grandson"), ("lifeline", "investigator"), ("eduardo-silva", "deceased"), ("cherisse-che", "appointee"), ("frontier-corps", "absorbed"), ("mercenary-syndicate", "subject")], ["wiki-torres-silva", "wiki-octane", "wiki-lifeline", "wiki-mercenary-syndicate", "wiki-timeline"])
V("williams-sendoff", O, "The Williams Sendoff", "Wraith finds morgue records of a body matching Jackson. Grieving, Bangalore fights with Loba and agrees to travel to Gridiron with Revenant. She holds a last family sendoff at the Hestia wreck, then decides to stay in the Outlands.", "Season 12 (2734)", 2734.57, ERA_G, 3, [("bangalore", "mourner"), ("wraith", "investigator"), ("loba", "rival"), ("revenant", "partner"), ("ims-hestia-01", "location")], ["wiki-bangalore", "wiki-wraith", "wiki-loba", "wiki-revenant", "wiki-timeline"])
V("newcastle-reveal", O, "Newcastle's debut and reveal (Season 13)", "Jackson takes the armor of Harris Valley's murdered hero Newcastle to pay the Forgotten Families. In Bangalore's 'final' match a huge beast attacks Storm Point, and afterward Anita takes off Newcastle's helmet and finds her brother.", "Season 13 (2734)", 2734.6, ERA_G, 4, [("newcastle", "subject"), ("bangalore", "discoverer"), ("forgotten-families", "blackmailer"), ("mirage", "teammate"), ("storm-point", "location")], ["wiki-newcastle", "wiki-bangalore", "wiki-storm-point", "wiki-timeline", "ea-newcastle"])
V("family-secrets", O, "Family Secrets in Harris Valley", "Wraith, Mirage and Bangalore fight the Forgotten Families at a warehouse, where a gauntleted mercenary recognizes Wraith. ARES files show that Dr. Renee Blasey oversaw his experimentation. Anita finds that Jackson has a family of his own.", "Season 13 (2734)", 2734.62, ERA_G, 3, [("wraith", "investigator"), ("mirage", "ally"), ("bangalore", "ally"), ("newcastle", "subject"), ("forgotten-families", "enemy"), ("harris-valley", "location")], ["wiki-wraith", "wiki-mirage", "wiki-bangalore", "wiki-newcastle"])
V("seer-interview", O, "Seer's Outlands TV ambush", "Lisa Stone turns Seer's interview into an attack on his character, and his standing on Boreas falls apart.", "Season 13 (2734)", 2734.63, ERA_G, 2, [("seer", "victim"), ("lisa-stone", "instigator")], ["wiki-seer", "wiki-timeline"])
V("vantage-rescue", O, "The GDS Vantage collapse (Season 14)", "Mara enters the wrecked prison ship, which collapses and crushes her. Xenia sets off a distress beacon to save her and is arrested. Mara and her bat Echo join the Games to publicize her mother's case.", "2734", 2734.7, ERA_G, 3, [("vantage", "victim"), ("xenia-contreras", "rescuer"), ("pagos", "location")], ["wiki-vantage", "wiki-timeline", "ea-vantage"])
V("jaime-attacked", O, "Jaime attacked; the source code stolen", "An unknown attacker takes Revenant's source code from Jaime and leaves him hanging and badly hurt, and Loba blames Revenant. Valkyrie meets Revenant in his Kings Canyon bunker and tells him the code was never sent to Gridiron, which begins a secret deal.", "Season 14 (2734)", 2734.75, ERA_G, 3, [("jaime", "victim"), ("loba", "avenger"), ("valkyrie", "negotiator"), ("revenant", "negotiator"), ("vantage", "witness"), ("revenant-source-code", "object")], ["wiki-loba", "wiki-valkyrie", "wiki-revenant", "wiki-timeline"])
V("bloodhound-fuse-kiss", O, "Bloodhound and Fuse get together", "While Fuse helps move Bloodhound's village from dying Talos to Storm Point, he admits his feelings. Bloodhound, afraid after losing Boone, accepts, and the two kiss.", "Season 14 (2734)", 2734.76, ERA_G, 2, [("bloodhound", "partner"), ("fuse", "partner"), ("vantage", "matchmaker")], ["wiki-bloodhound", "wiki-fuse", "wiki-timeline"])
V("friends-like-these", O, "Friends Like These", "Vantage visits the Legends to learn how to make friends and brings them to the party Mirage forgot to send invitations for. Along the way she sets off Wattson's repaired comm unit, which connects to Mila.", "Season 14 (2734)", 2734.78, ERA_G, 2, [("vantage", "subject"), ("mirage", "host"), ("wattson", "ally"), ("mila-alexander", "contact"), ("paradise-lounge", "location")], ["wiki-vantage", "wiki-mirage", "wiki-wattson"])
V("cleo-arena", O, "Hope becomes an arena (Season 15)", "Seer pitches bringing the Games to Boreas, and the Syndicate instead buys the colony of Hope on Cleo. The Cleo Recovery Council is pushed out, and terraformer Catalyst enters the Games.", "2734", 2734.85, ERA_G, 3, [("seer", "proposer"), ("octane", "planner"), ("torres-silva", "decider"), ("catalyst", "displaced"), ("cleo-recovery-council", "terminated"), ("broken-moon", "location")], ["wiki-broken-moon", "wiki-seer", "wiki-catalyst", "wiki-timeline", "ea-catalyst"])
V("reflections-of-the-moon", O, "Reflections of the Moon", "Angry Boreans attack Seer's parents' home, and Silva moves them to a safehouse. Catalyst shields Seer from a mob, and later at Encore the two come to understand each other.", "Season 15 (2734)", 2734.9, ERA_G, 2, [("seer", "subject"), ("catalyst", "ally"), ("octane", "ally"), ("torres-silva", "manipulator")], ["wiki-seer", "wiki-catalyst", "wiki-timeline"])
V("silva-gala-op", O, "Lifeline's operation at the Silva gala (Season 16)", "At the Games' anniversary party, Lifeline and Crypto steal data from Torres's computer and learn of a secret Syndicate Corps operation on Salvo. Lifeline and Fuse then clash with Cracked Talon remnants there.", "2735", 2735.05, ERA_G, 3, [("lifeline", "instigator"), ("crypto", "hacker"), ("octane", "distraction"), ("torres-silva", "target"), ("fuse", "guide"), ("cracked-talon", "enemy")], ["wiki-lifeline", "wiki-crypto", "wiki-fuse", "wiki-timeline"])
V("maggie-breakout", O, "Lifeline breaks Maggie out", "Lifeline disables a camera, attacks a guard and frees Maggie from prison. Maggie knocks out one of Lifeline's teeth as a cover story, and the two leave for Salvo.", "Season 16 (2735)", 2735.1, ERA_G, 3, [("lifeline", "instigator"), ("mad-maggie", "freed")], ["wiki-lifeline", "wiki-mad-maggie", "wiki-timeline"])
V("ballistic-takes-sons-place", O, "Ballistic takes his son's place (Season 17)", "When Nathaniel qualifies for the Games, August Brinkman storms a Syndicate facility and makes Torres Silva put him in instead. Nathaniel publicly smashes the ship model his father left him.", "2735", 2735.15, ERA_G, 3, [("ballistic", "instigator"), ("nathaniel-phua", "replaced"), ("torres-silva", "decider")], ["wiki-ballistic", "wiki-timeline", "ea-ballistic"])
V("salvo-bunker-raid", O, "Kill Code: the Salvo bunker", "Lifeline, Maggie and Loba raid a Silva-linked bunker on Salvo and find a facility making new Revenant bodies. Valkyrie gets them out, and Crypto starts decrypting the data.", "Season 17 (2735)", 2735.2, ERA_G, 3, [("lifeline", "ally"), ("mad-maggie", "ally"), ("loba", "ally"), ("valkyrie", "rescuer"), ("crypto", "decrypter"), ("torres-silva", "target")], ["wiki-lifeline", "wiki-loba", "wiki-mad-maggie", "wiki-valkyrie", "wiki-timeline"])
V("storm-point-storm", O, "The great storm at Storm Point", "A huge storm wrecks Storm Point's power plants, which supply Suotamo, and destroys the Hestia-01 wreck. Wattson rebuilds the grid.", "2735", 2735.22, ERA_G, 2, [("storm-point", "location"), ("wattson", "rebuilder"), ("ims-hestia-01", "destroyed")], ["wiki-storm-point", "wiki-wattson", "wiki-timeline"])
V("revenant-reborn", O, "Revenant reborn", "As Revenant's programming degrades, Hammond builds him a redesigned chassis on the secret Floor 17, and Torres Silva takes over the project. Revenant wakes up with different abilities and goes looking for whoever controls him.", "2735", 2735.25, ERA_G, 4, [("revenant", "subject"), ("hammond-robotics", "creator"), ("torres-silva", "controller")], ["wiki-revenant", "wiki-timeline", "ea-revenant"])
V("malta-facility-raid", O, "Raid on Hammond's Malta lab (Season 18)", "In an uneasy truce, Lifeline, Crypto, Revenant, Loba, Valkyrie and Maggie break into a Hammond lab to destroy the source code and fail. Silva takes it with Loba's lost staff, and Loba learns of Valkyrie's deal with Revenant.", "2735", 2735.3, ERA_G, 4, [("revenant", "ally"), ("loba", "ally"), ("valkyrie", "ally"), ("lifeline", "ally"), ("crypto", "ally"), ("mad-maggie", "ally"), ("torres-silva", "thief"), ("revenant-source-code", "object")], ["wiki-revenant", "wiki-loba", "wiki-valkyrie", "wiki-crypto", "wiki-timeline"])
V("conduit-joins", O, "Conduit joins the Games", "Rowenna Divina, powered by the battery of the Monarch Titan that saved her community, becomes the first resident of Nexus invited to the Games.", "Season 19 (2735)", 2735.32, ERA_G, 2, [("conduit", "competitor"), ("diwa", "objector"), ("nexus", "homeworld")], ["wiki-conduit", "wiki-timeline", "ea-conduit"])
V("torres-killed", O, "Death of Torres Silva", "Using a tracker Lifeline hid on Octane, the Legends follow the Silvas to a final facility. Revenant takes back his source code, finds he can control any of his shells, and kills Torres in front of Octane. Revenant's army attacks, and Valkyrie flies the Legends out and later breaks up with Loba.", "May 2735", 2735.35, ERA_G, 5, [("revenant", "instigator"), ("torres-silva", "victim"), ("octane", "witness"), ("loba", "witness"), ("valkyrie", "rescuer"), ("lifeline", "instigator"), ("revenant-source-code", "object")], ["wiki-revenant", "wiki-octane", "wiki-loba", "wiki-valkyrie", "wiki-mercenary-syndicate", "wiki-timeline"])
V("maggie-surrenders", O, "Maggie surrenders", "Back on Salvo, Maggie finds that the Syndicate has made the planet prosperous and that the Cracked Talon has disbanded. She turns herself in, and Bloodhound visits her and urges her to keep fighting.", "Season 19 (2735)", 2735.38, ERA_G, 2, [("mad-maggie", "subject"), ("cracked-talon", "disbanded"), ("bloodhound", "visitor")], ["wiki-mad-maggie", "wiki-bloodhound"])
V("torres-funeral-competition", O, "Torres's funeral and the collection contest (Season 20)", "Octane gives a conflicted eulogy, and Revenant mocks Forge's murder on Outlands TV. The Syndicate holds a contest for items from Torres's collection, and Octane wins the time gauntlet and gives it to Horizon.", "2735", 2735.4, ERA_G, 3, [("octane", "winner"), ("horizon", "recipient"), ("seer", "mourner"), ("conduit", "informant"), ("time-travel-device", "object"), ("revenant", "provocateur"), ("lisa-stone", "host")], ["wiki-octane", "wiki-horizon", "wiki-revenant", "wiki-timeline"])
V("alter-arrives", O, "Trouble on the Horizon: Alter arrives (Season 21)", "Parallel Olympuses flicker through portals, and one destroys Cleo's stasis net. Alter takes Horizon's time device along with Mirage and Lifeline, and crashes a drone into Humbert Labs, flooding Suotamo with gas. She then promises Horizon the missing piece.", "2735", 2735.5, ERA_G, 5, [("alter", "instigator"), ("horizon", "target"), ("mirage", "victim"), ("lifeline", "victim"), ("alternate-olympus", "phenomenon"), ("broken-moon", "location"), ("humbert-labs", "location"), ("e-district", "location")], ["wiki-alter", "wiki-horizon", "wiki-broken-moon", "wiki-e-district", "ea-upheaval-patch-notes", "wiki-timeline"])
V("alter-ark-shard-gift", O, "Alter gives Horizon an Ark shard", "After Alter tells Ash on Olympus that she plans to reunite Horizon with Newton, Ash vows to stop her. A desperate Horizon meets Alter, who gives her the stolen Ark shard as the power source her device needs.", "Season 21 (2735)", 2735.55, ERA_G, 4, [("alter", "giver"), ("horizon", "recipient"), ("ash", "opponent"), ("the-ark", "object"), ("time-travel-device", "object")], ["wiki-alter", "wiki-horizon", "wiki-ash", "wiki-timeline"])
V("e-district-arena", O, "E-District restored as an arena (Season 22)", "After the evacuation, the Syndicate buys and cleans up Suotamo's Electro District and opens it as a night-time neon arena.", "2735", 2735.6, ERA_G, 2, [("e-district", "location"), ("mercenary-syndicate", "owner")], ["wiki-e-district", "ea-shockwave-patch-notes"])
V("seer-replaced", O, "An alternate Seer appears", "While Seer lectures Octane about art in his apartment, he is briefly swapped with an alternate version of himself.", "Season 22 (2735)", 2735.62, ERA_G, 1, [("seer", "subject"), ("octane", "witness")], ["wiki-timeline"])
V("battle-for-the-past", O, "Battle for the Past: Ash cracks the Ark shard", "Ash breaks into Horizon's lab to destroy the Ark shard. Leigh begs her to let Horizon see Newton, but Ash wins the struggle and cracks the shard, which starts to radiate.", "Season 22 (2735)", 2735.65, ERA_G, 4, [("ash", "instigator"), ("horizon", "victim"), ("the-ark", "object")], ["wiki-ash", "wiki-timeline"])
V("lifeline-rift", O, "A rift swallows D.O.C. (Season 23)", "A rift in reality swallows D.O.C. Lifeline pulls it back at the cost of her hand, which she replaces with cybernetics before rebuilding the drone.", "Season 23", 2735.7, ERA_G, 2, [("lifeline", "subject"), ("doc-drone", "object")], ["wiki-lifeline", "ea-lifeline"])
V("fuse-proposes", O, "Fuse proposes to Bloodhound", "Fuse completes the courtship rites of Bloodhound's people and proposes with a blue-and-white copy of their axe, and Bloodhound accepts.", "Season 23", 2735.72, ERA_G, 2, [("fuse", "proposer"), ("bloodhound", "fiance")], ["wiki-fuse", "wiki-bloodhound"])
V("sparrow-cast-out", O, "Sparrow cast out of the Clessidra Rossa", "After a reckless act, Enea Guarino is cast out of the bounty-hunter clan and his family and leaves his sister Aurora behind. He hunts alone until a stranger recruits him for the Games.", "2736", 2736.0, ERA_G, 2, [("sparrow", "exile"), ("clessidra-rossa", "expeller"), ("aurora", "left-behind")], ["wiki-sparrow", "ea-sparrow", "wiki-season-25"])
V("redline-final", O, "The last Redline race", "Blisk offers an Apex Card to that season's Redline champion. Axle takes the lead from Weaver on the final lap with a wall-ride, and Weaver dies in the race. Axle wakes in hospital to Blisk handing her the card.", "Season 29", 2736.5, ERA_G, 2, [("axle", "winner"), ("weaver", "victim"), ("kuben-blisk", "recruiter"), ("salvo", "location")], ["wiki-axle", "ea-axle", "wiki-season-29", "ea-overclocked-patch-notes"])

# --- alternate timelines
V("imc-wins-frontier-war", "imc-victory", "The IMC wins the Frontier War", "In Wraith's home reality the IMC defeats the Frontier Militia, so it is still in power and still operates on Solace decades later.", "Frontier War", 2715.3, "Frontier War (IMC victory)", 5, [("imc", "victor"), ("frontier-militia", "defeated")], ["wiki-wraith", "wiki-voidwalker-wraith"])
V("project-wraith-alt", "imc-victory", "Project Wraith goes wrong", "ARES science pilot Renee Blasey volunteers as Subject 61137 for her own phase experiments with Amer Singh. The test erases her memory and fills her head with voices. Singh keeps experimenting on her against her will.", "before 2727", 2726.0, "IMC Rule", 4, [("wraith", "victim"), ("amer-singh", "instigator"), ("ares-division", "sponsor"), ("singh-labs", "location")], ["wiki-wraith", "wiki-amer-singh", "ea-wraith"])
V("voidwalker-rescue", "imc-victory", "The Voidwalker frees Blasey", "A white-armored Renee Blasey from the main reality comes through a portal to take revenge on Singh. She frees her captive self, gives her phase tech and a kunai, and stays to fight Singh and IMC guards.", "2727", 2727.3, "IMC Rule", 5, [("voidwalker-wraith", "rescuer"), ("wraith", "rescued"), ("amer-singh", "enemy"), ("imc", "enemy")], ["wiki-voidwalker-wraith", "wiki-wraith", "wiki-amer-singh"])
V("shadow-revenant-reign", "shadowfall", "The Shadow Revenant's reign", "Kaleb Cross of this reality becomes a simulacrum hitman like his counterpart and takes over a dark, alternate Kings Canyon.", "unknown", 2700.0, "Shadow Reign", 3, [("shadow-revenant", "ruler"), ("shadowfall-kings-canyon", "domain")], ["wiki-shadow-revenant"])
V("ash-head-sent", "shadowfall", "Ash's head lands in Shadowfall", "Under a deal with Blisk, Ash's head is thrown into an alternate dimension. It arrives in the Shadowfall dimension broken into nine pieces.", "before 2733", 2732.5, "Shadow Reign", 3, [("ash", "subject"), ("kuben-blisk", "instigator"), ("shadowfall-kings-canyon", "location")], ["wiki-ash", "wiki-kuben-blisk"])
V("pathfinder-in-shadowfall", "shadowfall", "Pathfinder strays into the beta plane", "Pathfinder ends up in a dark Kings Canyon ruled by an alternate Revenant.", "Season 3 (2733)", 2733.2, "Shadow Reign", 2, [("pathfinder", "visitor"), ("shadow-revenant", "ruler")], ["wiki-timeline", "wiki-pathfinder", "wiki-shadow-revenant"])
V("shadowfall-artifact-hunt", "shadowfall", "The artifact pieces are dug up", "Legends cross over through Wraith's portals to dig up the nine buried pieces, and Wattson is badly hurt on one trip. The Shadow Revenant resents them at first but helps them get the last piece.", "Season 5 (2733)", 2733.45, "Shadow Reign", 4, [("shadow-revenant", "reluctant-ally"), ("wraith", "portal-keeper"), ("wattson", "victim"), ("octane", "participant"), ("loba", "instigator"), ("pathfinder", "guide")], ["wiki-shadow-revenant", "wiki-wraith", "wiki-octane", "wiki-loba"])
V("alter-departs-home", "alter-multiverse", "Alter leaves her home dimension", "YingLing Lui uses cybernetic Void tech to leave her own reality. She drifts between worlds as 'Alter', stealing, fighting and doing mercenary work for fun.", "unknown", 2700.0, "Interdimensional Wandering", 3, [("alter", "subject"), ("the-void", "passage")], ["wiki-alter", "ea-alter"])
V("alter-dying-worlds", "alter-multiverse", "The common cause of the dying worlds", "Alter seeks out realities at the point of destruction and sometimes helps them fall. She notices that many were destroyed by the same person: Horizon.", "unknown", 2734.0, "Interdimensional Wandering", 4, [("alter", "witness"), ("horizon", "cause")], ["wiki-alter", "ea-alter", "ea-upheaval-patch-notes"])
V("alter-steals-shard", "alter-multiverse", "Alter steals an Ark shard", "Before reaching the Apex Games reality, Alter steals an Ark shard from a guarded facility. She also sabotages a company that was about to end world hunger.", "2735", 2735.45, "Interdimensional Wandering", 3, [("alter", "thief"), ("the-ark", "object")], ["wiki-alter", "wiki-timeline"])

# ---------------- RELATIONSHIPS ----------------
rels = []
def R(a, b, kind, desc, src, tl=None, since=None, until=None):
    rels.append({"source": a, "target": b, "kind": kind, "timeline": tl, "description": desc,
                 "since_event": since, "until_event": until, "sources": src})

# family
R("bangalore", "newcastle", "sibling", "Anita and Jackson Williams are siblings with a lifelong rivalry kept on a shared scorecard.", ["wiki-bangalore", "wiki-newcastle"])
R("zeke-williams", "bangalore", "sibling", "Zeke was the oldest Williams sibling. He died on Typhon.", ["wiki-bangalore"])
R("zeke-williams", "newcastle", "sibling", "Zeke was Jackson's oldest brother. He died on Typhon.", ["wiki-newcastle"])
R("marcos-andrade", "loba", "parent", "Marcos Andrade was Loba's father and taught her thieving.", ["wiki-loba"])
R("alanza-andrade", "loba", "parent", "Alanza Andrade was Loba's mother, also a thief.", ["wiki-loba"])
R("marcos-andrade", "alanza-andrade", "romance", "Marcos and Alanza were a married thieving couple.", ["wiki-loba"])
R("mystik", "caustic", "parent", "Katerina 'Mystik' Nox is Alexander Nox's mother.", ["wiki-caustic"])
R("mystik", "crypto", "parent", "Mystik adopted Tae Joon Park.", ["wiki-crypto"], None, "crypto-adopted")
R("mystik", "mila-alexander", "parent", "Mystik also adopted Mila, Tae Joon's foster sister.", ["wiki-crypto"], None, "crypto-adopted")
R("caustic", "crypto", "sibling", "Caustic and Crypto are adoptive brothers through Mystik, and Pathfinder works out the link.", ["wiki-caustic", "wiki-crypto"], None, "crypto-adopted")
R("crypto", "mila-alexander", "sibling", "Mila is Crypto's foster sister and former work partner.", ["wiki-crypto", "ea-crypto"])
R("luc-paquette", "wattson", "parent", "Luc Paquette was Wattson's father.", ["wiki-wattson"])
R("amelie-paquette", "wattson", "family", "Dr. Amélie Paquette was Wattson's grandmother.", ["wiki-wattson", "wiki-project-iris"])
R("horizon", "newton-somers", "parent", "Mary Somers is Newton's mother and wants to travel back in time to him.", ["wiki-horizon", "ea-horizon"])
R("aleki-gibraltar", "gibraltar", "family", "Dr. Aleki Gibraltar was Makoa Gibraltar's grandfather.", ["wiki-gibraltar", "wiki-project-iris"])
R("artur", "bloodhound", "family", "Artur was Bloodhound's uncle and adoptive guardian.", ["wiki-bloodhound"], None, "worlds-edge-flash-freeze")
R("artur", "bloodhound", "mentor", "Artur taught Bloodhound the Old Ways.", ["wiki-bloodhound", "ea-bloodhound"])
R("evelyn-witt", "mirage", "parent", "Evelyn Witt is Mirage's mother and taught him hologram tech.", ["wiki-mirage", "ea-mirage"])
R("cherisse-che", "lifeline", "parent", "Cherisse Che is Lifeline's estranged mother.", ["wiki-lifeline"])
R("darion-che", "lifeline", "parent", "Darion Che is Lifeline's estranged father and Chevrex's CEO.", ["wiki-lifeline"])
R("torres-silva", "eduardo-silva", "parent", "Torres Silva was the real Eduardo Silva's father.", ["wiki-torres-silva"])
R("eduardo-silva", "octane", "parent", "The real Eduardo Silva was Octane's father, who died years earlier.", ["wiki-octane", "wiki-torres-silva"])
R("torres-silva", "octane", "family", "Torres is Octane's grandfather who raised him while posing as his father Eduardo.", ["wiki-octane", "wiki-torres-silva", "ea-octane"])
R("ballistic", "nathaniel-phua", "parent", "August Brinkman is Nathaniel's estranged father.", ["wiki-ballistic", "ea-ballistic"])
R("sok-leng-phua", "nathaniel-phua", "parent", "Sok Leng is Nathaniel's mother.", ["wiki-ballistic"])
R("ballistic", "sok-leng-phua", "romance", "August and Sok Leng married after meeting in the Thunderdome and later separated.", ["wiki-ballistic", "ea-ballistic"], None, None, "kit-siang-death")
R("sok-leng-phua", "kit-siang-phua", "sibling", "Kit Siang was Sok Leng's brother and fighting partner.", ["wiki-ballistic"])
R("xenia-contreras", "vantage", "parent", "Xenia raised Mara alone on Págos.", ["wiki-vantage", "ea-vantage"])
R("diwa", "conduit", "sibling", "Diwa is Conduit's oldest sister.", ["wiki-conduit", "ea-conduit"])
R("sparrow", "aurora", "sibling", "Aurora is Sparrow's younger sister, left behind when he was exiled.", ["wiki-sparrow"])
R("viper", "valkyrie", "parent", "Viper was Valkyrie's father.", ["wiki-valkyrie", "ea-valkyrie"])
R("nik-gentile", "michael-gentile", "parent", "Nik is Michael Gentile's father.", ["wiki-gibraltar"])

# romance
R("bloodhound", "boone", "romance", "Boone was Bloodhound's lover. His death is why they seek honor.", ["wiki-bloodhound", "ea-bloodhound"], None, None, "boone-death")
R("bloodhound", "fuse", "romance", "Bloodhound and Fuse fell in love, moved in together and became engaged.", ["wiki-bloodhound", "wiki-fuse"], None, "bloodhound-fuse-kiss")
R("gibraltar", "nik-gentile", "romance", "Gibraltar and Nik were teenage boyfriends. They are now exes who are slowly reconnecting.", ["wiki-gibraltar", "ea-gibraltar"])
R("valkyrie", "loba", "romance", "Valkyrie and Loba dated until Valkyrie ended it after Revenant's attack.", ["wiki-valkyrie", "wiki-loba"], None, "loba-bangalore-just-friends", "torres-killed")
R("loba", "bangalore", "romance", "Loba and Bangalore have unresolved romantic feelings that their quarrels keep stalling.", ["wiki-loba", "wiki-bangalore"], None, "broken-ghost-quest")

# friendship / allies
R("lifeline", "octane", "friend", "Childhood friends from Olympus whose bond keeps breaking over the Silva family.", ["wiki-lifeline", "wiki-octane", "ea-octane"])
R("mirage", "pathfinder", "friend", "Pathfinder calls Mirage his best friend, and Mirage urged him to join the Games.", ["wiki-pathfinder", "wiki-mirage"])
R("mirage", "rampart", "friend", "Bickering roommates at the Paradise Lounge who come to care for each other.", ["wiki-mirage", "wiki-rampart"], None, "the-first-ship")
R("wraith", "mirage", "friend", "Mirage found Wraith's birthday in his mother's files, and they work together in Harris Valley.", ["wiki-wraith", "wiki-mirage"])
R("wraith", "wattson", "friend", "Wraith saved young Wattson, who remembers her as her ghost.", ["wiki-wraith", "wiki-wattson"], None, "wattson-ring-test")
R("wraith", "bangalore", "ally", "Wraith and Bangalore made a pact to uncover each other's pasts.", ["wiki-wraith", "wiki-bangalore"], None, "wraith-bangalore-pact")
R("wraith", "rampart", "friend", "Wraith found Rampart a new workshop inside the Paradise Lounge.", ["wiki-wraith", "wiki-rampart"])
R("crypto", "wattson", "friend", "Crypto trusted Wattson with his true identity, and she keeps his secrets.", ["wiki-crypto", "wiki-wattson"], None, "crypto-reveals-to-wattson")
R("caustic", "wattson", "other", "Caustic is fiercely protective of Wattson. She stopped his gas plot and made him promise to change.", ["wiki-caustic", "wiki-wattson"])
R("gibraltar", "bangalore", "friend", "Gibraltar and Bangalore are friends who share drinks.", ["wiki-gibraltar", "wiki-bangalore"])
R("gibraltar", "mirage", "friend", "Gibraltar confides in Mirage at the Paradise Lounge, and they rescue Michael together.", ["wiki-gibraltar", "wiki-mirage"])
R("gibraltar", "michael-gentile", "other", "Michael resents Gibraltar, who rescued him from Norlock Lake.", ["wiki-gibraltar"])
R("fuse", "mad-maggie", "friend", "Childhood friends who shared a golden grenade, until Fuse left for the Games.", ["wiki-fuse", "wiki-mad-maggie", "ea-mad-maggie"], None, None, "salvo-joins-fuse-arm")
R("fuse", "mad-maggie", "rival", "Maggie took Fuse's arm and calls him a traitor, but each still cares about the other.", ["wiki-fuse", "wiki-mad-maggie"], None, "salvo-joins-fuse-arm")
R("lifeline", "mad-maggie", "ally", "Lifeline teamed up with Maggie against Torres Silva and broke her out of prison.", ["wiki-lifeline", "wiki-mad-maggie"], None, "olympus-phase-drop")
R("lifeline", "crypto", "ally", "Crypto hacked Torres's records for Lifeline's operation.", ["wiki-lifeline", "wiki-crypto"], None, "silva-gala-op")
R("lifeline", "fuse", "ally", "Fuse took Lifeline to Salvo, then left when she crossed a line.", ["wiki-lifeline", "wiki-fuse"], None, "silva-gala-op")
R("loba", "jaime", "friend", "Jaime is Loba's longtime partner in crime and close friend.", ["wiki-loba"])
R("loba", "mad-maggie", "ally", "Loba joined Lifeline and Maggie's fight against Torres Silva.", ["wiki-loba", "wiki-mad-maggie"], None, "salvo-bunker-raid")
R("valkyrie", "rampart", "friend", "Bar friends. Rampart made Valkyrie's jetpack from the Northstar.", ["wiki-valkyrie", "wiki-rampart", "ea-valkyrie"])
R("seer", "rampart", "friend", "Former Arenas teammates with a long undefeated run together.", ["wiki-seer", "wiki-rampart"])
R("seer", "octane", "friend", "Octane planned the Boreas arena with Seer and stood by him when his parents were attacked.", ["wiki-seer", "wiki-octane"])
R("seer", "catalyst", "rival", "Catalyst blamed Seer for losing her home on Cleo.", ["wiki-catalyst", "wiki-seer"], None, "cleo-arena", "reflections-of-the-moon")
R("seer", "catalyst", "friend", "After talking at Encore they reached an understanding, and she will watch him try to do better.", ["wiki-catalyst", "wiki-seer"], None, "reflections-of-the-moon")
R("vantage", "mirage", "friend", "Mirage coached Vantage on friendship and media.", ["wiki-vantage", "wiki-mirage"], None, "friends-like-these")
R("vantage", "seer", "friend", "Seer agreed to be Vantage's friend.", ["wiki-vantage", "wiki-seer"], None, "friends-like-these")
R("horizon", "fuse", "friend", "Horizon comforted Fuse when Maggie joined the Games.", ["wiki-horizon", "wiki-fuse"])
R("octane", "horizon", "ally", "Octane won Torres's time gauntlet and gave it to Horizon.", ["wiki-octane", "wiki-horizon"], None, "torres-funeral-competition")
R("pathfinder", "ash", "friend", "Pathfinder sheltered the memory-wiped Ash and calls her his ex-girlfriend.", ["wiki-pathfinder", "wiki-ash"], None, "the-first-ship")
R("pathfinder", "rampart", "friend", "Rampart helped Pathfinder see through Revenant's lies and sent him to Blisk.", ["wiki-pathfinder", "wiki-rampart"])
R("pathfinder", "victor-maldera", "ally", "Pathfinder and Maldera escaped the Malta mobsters together.", ["wiki-pathfinder"], None, "fight-night")
R("pathfinder", "ballistic", "other", "Pathfinder once worked as Brinkman's butler and burned down a wing of his estate.", ["wiki-ballistic", "wiki-pathfinder"])
R("ballistic", "torres-silva", "friend", "Brinkman befriended Torres while believing he was Eduardo.", ["wiki-ballistic", "wiki-torres-silva"])
R("ballistic", "kit-siang-phua", "friend", "Thunderdome teammates. Brinkman's showboating led to Kit Siang's death.", ["wiki-ballistic", "ea-ballistic"], None, None, "kit-siang-death")
R("bloodhound", "mad-maggie", "other", "Bloodhound visited Maggie in prison and urged her not to give up.", ["wiki-bloodhound", "wiki-mad-maggie"], None, "maggie-surrenders")
R("mila-alexander", "wattson", "ally", "Mila secretly contacts Wattson through the repaired comm unit.", ["wiki-wattson"], None, "friends-like-these")
R("ash", "crypto", "ally", "Ash and Crypto formed a partnership against the Syndicate, and she calls him a pupil.", ["wiki-ash", "wiki-crypto"], None, "storm-point-arena")
R("kuben-blisk", "ash", "ally", "Fellow Apex Predators. Blisk reclaimed Ash and arranged for her head to be sent to Shadowfall.", ["wiki-kuben-blisk", "wiki-ash"])
R("horizon", "lillian-peck", "mentor", "Lillian Peck was Horizon's mentor and friend and cared for Newton.", ["wiki-horizon", "wiki-ash"])
R("cherisse-che", "torres-silva", "ally", "Cherisse is a close ally of Torres, who put her in charge of the Syndicate Corps.", ["wiki-torres-silva", "wiki-lifeline"])
R("revenant", "bangalore", "ally", "Revenant proposed sharing a ship to Gridiron, and Anita agreed before backing out.", ["wiki-revenant", "wiki-bangalore"], None, "williams-sendoff", "newcastle-reveal")
R("valkyrie", "revenant", "ally", "Valkyrie made a secret deal with Revenant to find and destroy his source code.", ["wiki-valkyrie", "wiki-revenant"], None, "jaime-attacked")
R("horizon", "alter", "ally", "Horizon accepted Alter's offer and the stolen Ark shard.", ["wiki-horizon", "wiki-alter"], None, "alter-ark-shard-gift")
R("voidwalker-wraith", "wraith", "ally", "The Voidwalker freed her alternate self and gave her phase tech.", ["wiki-voidwalker-wraith", "wiki-wraith"], None, "voidwalker-rescue")
R("kuben-blisk", "rampart", "other", "Blisk watched Rampart for a year and sponsored her entry into the Games.", ["wiki-rampart", "wiki-kuben-blisk"], None, "rampart-shop-burned")
R("kuben-blisk", "wattson", "other", "Blisk promised Wattson lifelong Syndicate support and let her join without qualifying.", ["wiki-wattson"])
R("kuben-blisk", "axle", "other", "Blisk set up the Redline prize and handed Axle her Apex Card.", ["wiki-axle", "ea-axle"], None, "redline-final")
R("kuben-blisk", "pathfinder", "other", "Blisk gave Pathfinder the records of Project Iris.", ["wiki-pathfinder"], None, "pathfinders-quest")
R("valkyrie", "kuben-blisk", "other", "Kairi once wanted Blisk dead for her father's death, but he gave her an Apex card instead.", ["wiki-valkyrie", "ea-valkyrie"], None, "valkyrie-confronts-blisk")
R("rampart", "valkyrie", "creator", "Rampart reforged Viper's Northstar into Valkyrie's jetpack and armor.", ["wiki-valkyrie"])

# rivals / enemies
R("crypto", "mirage", "rival", "Crypto and Mirage keep up a running 'kid' and 'old man' rivalry.", ["wiki-crypto", "wiki-mirage", "wiki-timeline"], None, "crypto-mirage-first-squad")
R("caustic", "crypto", "rival", "Caustic framed Crypto as the mole and resents his closeness to Wattson.", ["wiki-caustic", "wiki-crypto"], None, "broken-ghost-quest")
R("gibraltar", "caustic", "rival", "Gibraltar confronted Caustic for betraying the Legends.", ["wiki-gibraltar", "wiki-caustic"], None, "broken-ghost-quest")
R("revenant", "loba", "enemy", "Revenant killed Loba's parents. She keeps him alive out of revenge, and he swore to destroy what she loves.", ["wiki-revenant", "wiki-loba", "ea-loba", "ea-revenant"], None, "tenmei-massacre")
R("revenant", "marcos-andrade", "enemy", "Revenant killed Marcos Andrade on a Syndicate contract.", ["wiki-revenant", "wiki-loba"], None, "tenmei-massacre")
R("revenant", "forge", "enemy", "Revenant murdered Forge on live television.", ["wiki-revenant"], None, "forge-murdered")
R("revenant", "torres-silva", "enemy", "Torres seized control of Revenant, and Revenant killed him for it.", ["wiki-revenant", "wiki-torres-silva"], None, "revenant-reborn", "torres-killed")
R("revenant", "quentin-willis", "enemy", "Revenant impaled Boss Willis after working for him.", ["wiki-revenant"], None, "overtime")
R("revenant", "ash", "enemy", "Revenant cracked Ash's faceplate in a twisted mercy attempt.", ["wiki-revenant", "wiki-ash"], None, "ash-awakened")
R("revenant", "pathfinder", "rival", "Revenant tricked Pathfinder into believing he killed his creators.", ["wiki-revenant", "wiki-pathfinder"], None, "pathfinders-quest")
R("revenant", "hammond-robotics", "enemy", "Revenant swore revenge on Hammond for turning him into a simulacrum.", ["wiki-revenant", "ea-revenant"], None, "tenmei-massacre")
R("ash", "horizon", "enemy", "Ash betrayed Horizon at the black hole and wants to keep her from Newton.", ["wiki-ash", "wiki-horizon", "ea-ash"], None, "somers-betrayed")
R("ash", "amelie-paquette", "enemy", "Reid cut off Amélie's hand, and Amélie killed Reid's human body.", ["wiki-ash", "wiki-project-iris"], None, "phase-runner-incident")
R("ash", "wattson", "enemy", "Ash wants to end the Paquette bloodline to silence Leigh.", ["wiki-ash", "wiki-wattson"], None, "ash-attacks-wattson")
R("ash", "alter", "rival", "Ash vowed to stop Alter from helping Horizon change the past.", ["wiki-ash", "wiki-alter"], None, "alter-ark-shard-gift")
R("alter", "mirage", "enemy", "Alter abducted and beat Mirage while stealing Horizon's device.", ["wiki-alter", "wiki-mirage"], None, "alter-arrives")
R("alter", "lifeline", "enemy", "Alter abducted and beat Lifeline while stealing Horizon's device.", ["wiki-alter", "wiki-lifeline"], None, "alter-arrives")
R("ash", "newton-somers", "mentor", "Reid mentored Newton when he interned with the Group.", ["wiki-ash", "wiki-horizon"])
R("jack-cooper", "viper", "enemy", "Cooper and BT-7274 killed Viper on Typhon.", ["wiki-valkyrie", "wiki-frontier-war"], None, "battle-of-typhon")
R("jack-cooper", "ash", "enemy", "Cooper crushed Ash's simulacrum body on Typhon.", ["wiki-ash"], None, "battle-of-typhon")
R("jack-cooper", "kuben-blisk", "enemy", "Blisk fought Cooper on Typhon and offered him a place in the Predators.", ["wiki-kuben-blisk"], None, "battle-of-typhon")
R("bangalore", "scryer", "enemy", "Anita and Jackson killed Scryer, and she took his data knife.", ["wiki-bangalore", "wiki-newcastle"], None, "hestia-crash")
R("newcastle", "forgotten-families", "enemy", "The Forgotten Families blackmail Jackson into fighting to pay Harris Valley's debts.", ["wiki-newcastle", "ea-newcastle"], None, "newcastle-reveal")
R("rampart", "the-sisters", "enemy", "Big Sister's gang burned down Rampart's shop and still harasses her.", ["wiki-rampart"], None, "rampart-shop-burned")
R("caustic", "franklin-humbert", "enemy", "Caustic murdered his superior Humbert.", ["wiki-caustic"], None, "humbert-labs-murder")
R("victor-maldera", "caustic", "enemy", "Maldera has hunted Nox since the Humbert Labs fire.", ["wiki-caustic"])
R("lifeline", "torres-silva", "enemy", "Lifeline exposed Torres and worked to bring him down.", ["wiki-lifeline", "wiki-torres-silva"], None, "legacy-antigen")
R("mad-maggie", "torres-silva", "enemy", "Torres framed Maggie for the Olympus drop, and she joined the plot against him.", ["wiki-mad-maggie", "wiki-torres-silva"], None, "olympus-phase-drop")
R("mad-maggie", "mercenary-syndicate", "enemy", "Maggie waged an independence war against the Syndicate.", ["wiki-mad-maggie", "ea-mad-maggie"])
R("crypto", "mercenary-syndicate", "enemy", "Crypto seeks revenge on the Syndicate for framing him.", ["wiki-crypto", "ea-crypto"], None, "crypto-framed")
R("valkyrie", "kuben-blisk", "rival", "Kairi blamed Blisk for her father's death until they met.", ["wiki-valkyrie", "ea-valkyrie"], None, "battle-of-typhon", "valkyrie-confronts-blisk")
R("bangalore", "wraith", "rival", "Bangalore blamed Wraith for losing Jackson's message until the truth came out.", ["wiki-bangalore", "wiki-wraith"], None, "anita-singh-labs-drive", "wraith-bangalore-pact")
R("lisa-stone", "seer", "enemy", "Lisa Stone ambushed Seer on air to wreck his reputation.", ["wiki-seer"], None, "seer-interview")
R("axle", "weaver", "rival", "Weaver was Axle's only true rival in Redline.", ["wiki-axle", "ea-axle"], None, None, "redline-final")
R("wraith", "amer-singh", "enemy", "Singh kept Blasey captive and experimented on her.", ["wiki-wraith", "wiki-amer-singh"], "imc-victory", "project-wraith-alt")
R("voidwalker-wraith", "amer-singh", "enemy", "The Voidwalker crossed realities seeking revenge on Singh.", ["wiki-voidwalker-wraith", "wiki-amer-singh"], None, "voidwalker-rescue")
R("frontier-militia", "imc", "enemy", "The Militia and the IMC fought the Titan Wars and the Frontier War.", ["wiki-frontier-war", "wiki-imc"])
R("catalyst", "mercenary-syndicate", "rival", "The Syndicate's takeover of Hope ended Catalyst's job and home.", ["wiki-catalyst", "ea-catalyst"], None, "cleo-arena")

# variants
R("revenant", "shadow-revenant", "variant", "The Shadow Revenant is the Shadowfall dimension's Kaleb Cross.", ["wiki-shadow-revenant"])
R("wraith", "voidwalker-wraith", "variant", "Two versions of Renee Blasey from different realities.", ["wiki-voidwalker-wraith", "wiki-wraith"])
R("olympus", "alternate-olympus", "variant", "Parallel Olympuses broke into the main reality in 2735.", ["wiki-olympus", "wiki-broken-moon"])
R("kings-canyon", "shadowfall-kings-canyon", "variant", "Shadowfall holds a dark alternate Kings Canyon.", ["wiki-shadow-revenant", "wiki-loba"])
R("shadow-revenant", "pathfinder", "other", "Pathfinder stumbled into the Shadow Revenant's realm.", ["wiki-pathfinder", "wiki-timeline"], "shadowfall", "pathfinder-in-shadowfall")
R("shadow-revenant", "loba", "ally", "The Shadow Revenant helped Loba's group recover the final artifact piece.", ["wiki-shadow-revenant"], "shadowfall", "shadowfall-artifact-hunt")

# creators
R("project-iris", "pathfinder", "creator", "The Group built Pathfinder to run the branthium refinery.", ["wiki-pathfinder", "wiki-project-iris"], None, "pathfinder-activated")
R("newton-somers", "pathfinder", "creator", "Newton was one of Pathfinder's creators.", ["wiki-pathfinder", "wiki-horizon"])
R("ash", "pathfinder", "creator", "Reid proposed the MRVN and is listed among his creators.", ["wiki-pathfinder", "wiki-ash"])
R("amelie-paquette", "pathfinder", "creator", "Amélie helped build Pathfinder and authorized his self-destruct.", ["wiki-pathfinder"])
R("aleki-gibraltar", "pathfinder", "creator", "Aleki Gibraltar was one of Pathfinder's creators.", ["wiki-pathfinder"])
R("hammond-robotics", "revenant", "creator", "Hammond Robotics built and rebuilt Revenant's simulacrum bodies.", ["wiki-revenant", "wiki-hammond-robotics"], None, "revenant-first-boot")
R("heinrich-hammond", "hammond-robotics", "creator", "Heinrich Hammond founded Hammond Robotics.", ["wiki-hammond-robotics"], None, "hammond-engineering-founded")
R("heinrich-hammond", "imc", "creator", "Hammond Engineering grew into the IMC.", ["wiki-imc"], None, "imc-formed")
R("wattson", "the-ring", "creator", "Wattson designed the Ring.", ["wiki-wattson", "ea-wattson"], None, "wattson-ring-test")
R("horizon", "branthium", "creator", "Somers theorized and first collected branthium.", ["wiki-horizon", "ea-horizon"], None, "somers-betrayed")
R("lillian-peck", "project-iris", "creator", "Lillian Peck founded Project Iris.", ["wiki-project-iris"], None, "project-iris-founded")
R("lillian-peck", "olympus", "creator", "Lillian Peck paid for Olympus.", ["wiki-olympus"], None, "olympus-built")
R("torres-silva", "silva-pharmaceuticals", "creator", "Torres founded Silva Pharmaceuticals around Stim.", ["wiki-torres-silva"])
R("mercenary-syndicate", "apex-games", "creator", "The Syndicate created the Apex Games under the 2723 treaty.", ["wiki-mercenary-syndicate", "wiki-apex-games"], None, "syndicate-treaty")

# membership / leadership
R("kuben-blisk", "apex-predators", "leader", "Blisk leads the Apex Predators.", ["wiki-apex-predators", "wiki-kuben-blisk"])
R("kuben-blisk", "apex-games", "leader", "Blisk is commissioner of the Apex Games.", ["wiki-kuben-blisk", "wiki-apex-games"], None, "apex-games-begin")
R("ash", "apex-predators", "member", "Ash is a longtime Apex Predator.", ["wiki-apex-predators", "wiki-ash"])
R("viper", "apex-predators", "member", "Viper was an Apex Predators pilot.", ["wiki-apex-predators", "wiki-valkyrie"])
R("apex-predators", "mercenary-syndicate", "member", "The Apex Predators are the Syndicate's elite unit.", ["wiki-apex-predators", "wiki-mercenary-syndicate"])
R("torres-silva", "mercenary-syndicate", "leader", "Torres ruled the Syndicate as its 'One Voice'.", ["wiki-mercenary-syndicate", "wiki-torres-silva"], None, "torres-revealed", "torres-killed")
R("torres-silva", "silva-pharmaceuticals", "leader", "Torres ran Silva Pharmaceuticals under Eduardo's name.", ["wiki-torres-silva"])
R("cherisse-che", "frontier-corps", "leader", "Cherisse heads the militarized Syndicate Corps.", ["wiki-lifeline", "wiki-timeline"], None, "torres-revealed")
R("darion-che", "chevrex", "leader", "Darion Che is CEO of Chevrex.", ["wiki-lifeline"])
R("lifeline", "frontier-corps", "member", "Lifeline joined the Frontier Corps and fights to fund it.", ["wiki-lifeline", "ea-lifeline"])
R("mad-maggie", "cracked-talon", "leader", "Maggie founded and led the Cracked Talon.", ["wiki-mad-maggie", "ea-mad-maggie"], None, None, "maggie-surrenders")
R("gibraltar", "saras", "member", "Gibraltar is a SARAS search-and-rescue operator.", ["wiki-gibraltar", "ea-gibraltar"])
R("revenant", "mercenary-syndicate", "member", "Revenant served for centuries as the Syndicate's hitman.", ["wiki-revenant", "ea-revenant"], None, "revenant-first-boot")
R("bangalore", "imc", "member", "Bangalore is a lifelong IMC soldier.", ["wiki-bangalore", "ea-bangalore"])
R("newcastle", "imc", "member", "Jackson was an IMC officer until he deserted at Gridiron.", ["wiki-newcastle"], None, None, "battle-of-gridiron")
R("jack-cooper", "frontier-militia", "member", "Jack Cooper is a Militia pilot.", ["wiki-ash", "wiki-frontier-war"])
R("ares-division", "imc", "member", "ARES is the IMC's research division.", ["wiki-frontier-war", "wiki-wraith"])
R("wraith", "ares-division", "member", "In her home reality, Blasey was an ARES science pilot.", ["wiki-wraith", "ea-wraith"], "imc-victory")
R("amer-singh", "ares-division", "member", "Singh was an ARES scientist.", ["wiki-amer-singh"], "imc-victory")
R("voidwalker-wraith", "ares-division", "member", "The main reality's Blasey also served ARES.", ["wiki-voidwalker-wraith"])
R("hammond-robotics", "imc", "member", "Hammond Robotics was an IMC subsidiary until the IMC withdrew.", ["wiki-hammond-robotics"], None, None, "imc-leaves-outlands")
R("project-iris", "chevrex", "other", "Chevrex and Silva Pharmaceuticals helped fund Pathfinder's construction.", ["wiki-pathfinder"])
R("amelie-paquette", "project-iris", "member", "Amélie was the Group's geologist.", ["wiki-project-iris"])
R("newton-somers", "project-iris", "member", "Newton interned with Project Iris.", ["wiki-project-iris"])
R("aleki-gibraltar", "project-iris", "member", "Aleki was a Project Iris scientist.", ["wiki-project-iris"])
R("ash", "project-iris", "member", "Reid infiltrated Project Iris as a scientist.", ["wiki-project-iris", "ea-ash"])
R("catalyst", "cleo-recovery-council", "member", "Catalyst was a CRC terraformer in Hope.", ["wiki-catalyst"], None, "margo-bombing", "cleo-arena")
R("sparrow", "clessidra-rossa", "member", "Sparrow was raised in the clan and cast out.", ["wiki-sparrow", "ea-sparrow"], None, None, "sparrow-cast-out")
R("caustic", "humbert-labs", "member", "Nox worked at Humbert Labs as a researcher.", ["wiki-caustic", "ea-caustic"], None, None, "humbert-labs-murder")
R("luc-paquette", "mercenary-syndicate", "member", "Luc was the Syndicate's engineer for the Games' power grid.", ["wiki-wattson"], None, "syndicate-treaty")
R("mila-alexander", "mercenary-syndicate", "member", "Mila now works undercover inside the Syndicate.", ["wiki-wattson", "wiki-timeline"])
R("quentin-willis", "mercenary-syndicate", "member", "Willis was a Syndicate official.", ["wiki-timeline"])
R("forge", "hammond-robotics", "member", "Forge was Hammond's sponsored contender.", ["wiki-hammond-robotics"])
R("sandringham-kelly", "mercenary-syndicate", "ally", "Kelly signed Salvo into Syndicate Space.", ["wiki-timeline", "ea-mad-maggie"], None, "salvo-joins-fuse-arm")
R("loba", "hammond-robotics", "ally", "Loba traded Ash's head to Hammond for the location of Revenant's source code.", ["wiki-loba", "wiki-ash"], None, "skull-town-collapse")

# objects
R("loba", "revenant-source-code", "other", "Loba found the source code and refused to destroy it.", ["wiki-loba", "wiki-revenant"], None, "loba-hides-source-code")
R("jaime", "revenant-source-code", "other", "Jaime secretly kept the source code until it was stolen.", ["wiki-revenant", "wiki-timeline"], None, "loba-hides-source-code", "jaime-attacked")
R("torres-silva", "medusa-vines", "other", "Torres sent the vine-laden Icarus fleet to Olympus.", ["wiki-torres-silva", "wiki-olympus"], None, "legacy-antigen")
R("valkyrie", "vipers-northstar", "other", "Valkyrie salvaged her father's Northstar from Typhon.", ["wiki-valkyrie"], None, "valkyrie-typhon-salvage")
R("lifeline", "doc-drone", "other", "D.O.C. is Lifeline's healing drone, rebuilt after the rift.", ["wiki-lifeline", "ea-lifeline"])
R("alter", "the-ark", "other", "Alter stole an Ark shard and gave it to Horizon.", ["wiki-alter", "wiki-horizon"], None, "alter-steals-shard")
R("newcastle", "ims-hestia-01", "leader", "Jackson commanded the IMS Hestia-01.", ["wiki-newcastle"])

for e in entities:
    pass

data = {
    "game": {"slug": "apex-legends", "name": "Apex Legends",
             "calendar": "The lore uses plain Gregorian years (CE) in the 2100s-2700s of the Titanfall universe; seasons 0-7 fall in 2733, 8-15 in 2734 and 16 onward in 2735.",
             "description": "A free-to-play hero battle royale set in the Outlands, a fringe region of the Titanfall universe, about 20 years after the Frontier War. The Mercenary Syndicate stages the Apex Games, a televised bloodsport, and each Legend has a backstory tied to corporate wars, simulacra, and travel between realities."},
    "wiki": {"base": "https://apexlegends.wiki.gg", "api": "https://apexlegends.wiki.gg/api.php",
             "license": "CC BY-NC-SA 4.0 (wiki.gg siteinfo rightsinfo); apexlegends.fandom.com, also still edited in 2026, is CC BY-SA 3.0",
             "notes": "Both wikis showed recent edits in October 2026. apexlegends.wiki.gg is the better-kept lore wiki and was used. The API works with action=parse&page=<Page>&prop=wikitext&format=json&redirects=1, but needs a descriptive User-Agent (a generic 'Mozilla/5.0' UA got a wiki.gg block page). Most useful pages: Timeline (dated table to Season 22), '<Legend> (character)' lore pages, Mercenary Syndicate, Kuben Blisk, Torres Silva, Project Iris, Frontier War, Interstellar Manufacturing Corporation, Hammond Robotics, map pages (Kings Canyon, World's Edge, Olympus, Storm Point, Broken Moon, E-District), Shadow Revenant, Voidwalker Wraith, Amer Singh, Void, Minor characters. Season pages are mostly battle-pass data with little lore. Official bios come from ea.com characters-hub pages: the bio text is in the embedded JSON 'description' field, not the rendered HTML."},
    "sources": sources,
    "timelines": timelines,
    "entities": entities,
    "events": events,
    "relationships": rels,
}

# ---------- validation ----------
errs = []
src_keys = [s["key"] for s in sources]
assert len(src_keys) == len(set(src_keys)), "dup source keys"
srcset = set(src_keys)
tls = {t["slug"] for t in timelines}
ents = [e["slug"] for e in entities]
dups = {x for x in ents if ents.count(x) > 1}
if dups: errs.append(f"dup entities {dups}")
entset = set(ents)
evs = [e["slug"] for e in events]
d2 = {x for x in evs if evs.count(x) > 1}
if d2: errs.append(f"dup events {d2}")
evset = set(evs)
slug_re = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
for s in list(entset) + list(evset) + list(tls):
    if not slug_re.match(s): errs.append("bad slug " + s)
if entset & evset: errs.append(f"entity/event slug overlap {entset & evset}")
for t in timelines:
    if t["parent"] and t["parent"] not in tls: errs.append("bad parent " + t["slug"])
for e in entities:
    if e["timeline"] and e["timeline"] not in tls: errs.append("ent tl " + e["slug"])
    if e["variant_of"] and e["variant_of"] not in entset: errs.append("variant " + e["slug"])
    if not e["sources"]: errs.append("nosrc " + e["slug"])
    for s in e["sources"]:
        if s not in srcset: errs.append(f"ent src {e['slug']} {s}")
for v in events:
    if v["timeline"] not in tls: errs.append("ev tl " + v["slug"])
    for p in v["participants"]:
        if p["entity"] not in entset: errs.append(f"ev part {v['slug']} {p['entity']}")
    for s in v["sources"]:
        if s not in srcset: errs.append(f"ev src {v['slug']} {s}")
    if not (1 <= v["importance"] <= 5): errs.append("imp " + v["slug"])
for r in rels:
    for k in ("source", "target"):
        if r[k] not in entset: errs.append(f"rel {k} {r[k]}")
    if r["timeline"] and r["timeline"] not in tls: errs.append(f"rel tl {r}")
    for k in ("since_event", "until_event"):
        if r[k] and r[k] not in evset: errs.append(f"rel {k} {r[k]}")
    if not r["sources"]: errs.append("rel nosrc")
    for s in r["sources"]:
        if s not in srcset: errs.append(f"rel src {r['source']}->{r['target']} {s}")
    if r["kind"] not in "family|sibling|parent|romance|ally|friend|rival|enemy|mentor|member|leader|creator|variant|other".split("|"):
        errs.append("rel kind " + r["kind"])
# unused sources
used = set()
for coll in (entities, events, rels):
    for x in coll: used.update(x["sources"])
unused = srcset - used
if errs:
    print("ERRORS:"); [print(" ", e) for e in errs]; sys.exit(1)
if unused:
    data["sources"] = [s for s in sources if s["key"] in used]
    print("dropped unused sources:", sorted(unused))
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("entities", len(entities), "events", len(events), "relationships", len(rels), "timelines", len(timelines), "sources", len(data["sources"]))
from collections import Counter
print(Counter(e["kind"] for e in entities)); print(Counter(v["timeline"] for v in events)); print(Counter(r["kind"] for r in rels))
