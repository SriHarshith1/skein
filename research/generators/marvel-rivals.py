import json, urllib.parse

OUT = "/Users/kaneki/Desktop/workspace/Projects - Scrap/lorelines/research/marvel-rivals.json"
W = "https://marvelrivals.fandom.com/wiki/"


def wurl(title):
    return W + urllib.parse.quote(title.replace(" ", "_"), safe="/:")


SRC = [
    ("official-home", "https://www.marvelrivals.com/", "Marvel Rivals official site: map and season descriptions", "official"),
]
WIKI_PAGES = [
    ("wiki-te", "Timestream Entanglement"),
    ("wiki-chronoverses", "Chronoverses"),
    ("wiki-present", "Present Timeline"),
    ("wiki-2099", "2099 Timeline"),
    ("wiki-mosaic", "Mosaic Timeline"),
    ("wiki-collapsed", "Collapsed Timeline"),
    ("wiki-misc", "Miscellaneous Chronoverses"),
    ("wiki-watercolor", "Watercolor Timeline"),
    ("wiki-zombies", "Marvel Zombies Timeline"),
    ("wiki-doomsday", "Path to Doomsday Timeline"),
    ("wiki-trd", "Timestream Reintegration Device"),
    ("wiki-chronovium", "Chronovium"),
    ("wiki-galacta", "Galacta"),
    ("wiki-doom", "Doctor Doom"),
    ("wiki-doom2099", "Doom 2099"),
    ("wiki-seasons", "Seasons"),
    ("wiki-heroes", "Heroes"),
    ("wiki-s0", "Season 0: Dooms' Rise/Lore"),
    ("wiki-s1", "Season 1: Eternal Night Falls/Lore"),
    ("wiki-s2", "Season 2: Hellfire Gala/Lore"),
    ("wiki-s3", "Season 3: The Abyss Awakens/Lore"),
    ("wiki-s4", "Season 4: Heart of the Dragon/Lore"),
    ("wiki-s5", "Season 5: Love is a Battlefield/Lore"),
    ("wiki-s6", "Season 6: Night at the Museum/Lore"),
    ("wiki-s7", "Season 7: The Hunt Is On/Lore"),
    ("wiki-blood-hunt", "Blood Hunt/Lore"),
    ("wiki-s8", "Season 8: Sins of Alchemax/Lore"),
    ("wiki-s9", "Season 9: The Mystery of Thebes/Lore"),
    ("wiki-s10", "Season 10: Butcher's Blasphemy/Lore"),
    ("wiki-mrf-lore", "Mister Fantastic/Lore"),
    ("wiki-cap-lore", "Captain America/Lore"),
    ("wiki-bp-lore", "Black Panther/Lore"),
    ("wiki-starlord-lore", "Star-Lord/Lore"),
    ("wiki-venom-lore", "Venom/Lore"),
    ("wiki-adam-lore", "Adam Warlock/Lore"),
    ("wiki-hulk-lore", "Hulk/Lore"),
    ("wiki-ironfist-lore", "Iron Fist/Lore"),
    ("wiki-gorr", "Gorr"),
    ("wiki-moongirl", "Moon Girl"),
    ("wiki-whitefox", "White Fox"),
]
sources = [{"key": k, "url": u, "title": t, "publisher": p} for k, u, t, p in SRC]
for k, t in WIKI_PAGES:
    sources.append({"key": k, "url": wurl(t), "title": t + " - Marvel Rivals Wiki", "publisher": "wiki"})

# ---------------------------------------------------------------- timelines
timelines = [
    dict(slug="present", name="Present Timeline", kind="canon", parent=None, branch_note=None,
         description="The present-day (mid-2020s) Chronoverse where most playable heroes come from. New York City is its focal point, and it suffers the Eternal Night, the Alchemax incursion and the Blood Hunt."),
    dict(slug="timeline-2099", name="2099 Timeline", kind="alternate", parent="present",
         branch_note="A separate future reality set in the year 2099, home of Doom 2099. Krakoa and Arakko were carried into it by a timestorm during the Timestream Entanglement.",
         description="A techno-dystopia ruled by megacorporations such as Alchemax. It holds Tokyo 2099, Nueva York, the Web of Life and Destiny and the time-displaced mutant nation of Krakoa."),
    dict(slug="mosaic", name="Mosaic Timeline", kind="alternate", parent="present",
         branch_note="One of the four main Chronoverses formed by the Timestream Entanglement; its space-time is described as unstable.",
         description="A mostly cosmic reality of interstellar travel and alien threats. It contains the Intergalactic Empire of Wakanda, the Guardians of the Galaxy and Knull's prison planet Klyntar."),
    dict(slug="collapsed", name="Collapsed Timeline", kind="alternate", parent="present",
         branch_note="A present-day reality ravaged by a war between gods and demons. It was first called the Collapsing Timeline and was renamed from Season 9.",
         description="A dying world of divine and demonic war, where even gods die. It is the home of Scarlet Witch, Magik, Hulk, Daredevil, Elsa Bloodstone, Gorr and Apocalypse's Thebes."),
    dict(slug="watercolor", name="Watercolor Timeline", kind="alternate", parent="present",
         branch_note="Unofficial wiki name. A minor Chronoverse that the Timestream Entanglement destroyed soon after it began.",
         description="Psylocke's home reality, loosely based on the Demon Days universe. The Collector sent Deadpool to take Psylocke from it before it fell."),
    dict(slug="jeff-timeline", name="Jeff's Timeline", kind="alternate", parent="present",
         branch_note="Unofficial wiki name for an unnamed reality on the verge of destruction after the Entanglement.",
         description="The home of Jeff the Land Shark, Gwenpool and a local Deadpool. The Present Timeline's Deadpool took Jeff from it for the Collector."),
    dict(slug="venom-timeline", name="Venom's Timeline", kind="alternate", parent="present",
         branch_note="Unofficial wiki name for an unknown reality devastated by Knull's forces.",
         description="The uncertain home reality of Venom. The Entanglement linked Venom to the Mosaic Timeline's symbiote hivemind, so Eddie and the symbiote are unsure where they came from."),
    dict(slug="marvel-zombies", name="Marvel Zombies Timeline", kind="au", parent="present",
         branch_note="Unofficial wiki name for a minor Chronoverse on the brink of destruction after the Entanglement.",
         description="A reality where a Quantum Realm virus zombified much of the world. Its zombie Scarlet Witch, the Queen of the Dead, hunts for a zombie symbiote called K-44."),
    dict(slug="path-to-doomsday", name="Path to Doomsday Timeline", kind="au", parent="present",
         branch_note="Unofficial wiki name for the setting of the multi-season Path to Doomsday event, inspired by the MCU Infinity Saga.",
         description="A reality modeled loosely on the Avengers films, seen through the eyes of the God of Stories, in which the heroes move toward a clash with Doctor Doom."),
    dict(slug="beyond-the-chronoverses", name="Realms Beyond the Chronoverses", kind="alternate", parent=None,
         branch_note="Grouping used in this file, not an in-game name. The wiki describes the God Quarry as unbound to any timeline and Omnipotence City as independent of the Chronoverse; the Elders' merged domain also sits outside the four main realities.",
         description="Cosmic domains outside any single Chronoverse: the merged Collector's Gallery and Grand Garden, the God Quarry, Omnipotence City and the House of Ideas."),
]

# ---------------------------------------------------------------- entities
entities = []


def E(slug, name, kind, tl, summary, srcs, var=None, aliases=None):
    entities.append(dict(slug=slug, name=name, kind=kind, timeline=tl, variant_of=var,
                         aliases=aliases or [], summary=summary, sources=srcs))


P = None  # canon / present timeline
T99 = "timeline-2099"
MO = "mosaic"
CO = "collapsed"
BY = "beyond-the-chronoverses"

# --- playable heroes (54)
E("adam-warlock", "Adam Warlock", "character", P,
  "A golden cosmic guardian who sealed himself in a cocoon when the Timestream Entanglement struck and drifted into the Mosaic reality, where Bast spoke to him. His cosmic senses led him to Klyntar, and later he helped work out Gorr's Godbomb plan.",
  ["wiki-present", "wiki-adam-lore", "wiki-s10"])
E("angela", "Angela", "character", P,
  "Odin's daughter, raised as an angel in the hidden Tenth Realm of Heven. The Entanglement swept Heven into the Collapsed Timeline, where she became its queen, and she now hunts for her infant sister Laussa.",
  ["wiki-present", "wiki-s4", "wiki-s10"])
E("black-cat", "Black Cat", "character", P,
  "Felicia, a thief whom Mayor Fisk hired to steal the Tablet of Life and Time. She gave Fisk a replica, traded the real Tablet to Doctor Doom to free the Thieves Guild, and then became the Guild's leader.",
  ["wiki-s7", "wiki-present"], aliases=["Felicia"])
E("black-panther", "Black Panther", "character", MO,
  "T'Challa, ruler of the Intergalactic Empire of Wakanda, who trusts neither Doom. On a trip to the Present Timeline to deliver a Heart-Shaped Herb he was turned into a vampire by Dracula's Blood Chronovium but kept his own mind.",
  ["wiki-mosaic", "wiki-bp-lore", "wiki-s1"], aliases=["T'Challa"])
E("black-widow", "Black Widow", "character", T99,
  "Natalia Romanova, kept alive into 2099 by a life-extending serum. She turned the Red Room into her own spy network, leads the Resistance and freed the frozen Captain America from Alchemax.",
  ["wiki-2099", "wiki-s0"], aliases=["Natasha Romanoff", "Natalia Romanova"])
E("blade", "Blade", "character", P,
  "The Daywalker vampire hunter, captured and drained by Dracula during the Eternal Night. After treatment in Wakanda he fought Hela on Klyntar with the Sword of Dracula and later turned Dracula to stone in the Blood Hunt.",
  ["wiki-present", "wiki-s1", "wiki-s3", "wiki-blood-hunt"])
E("captain-america", "Captain America", "character", T99,
  "Steve Rogers of the 2099 Timeline, frozen since World War II and thawed in 2099 by Black Widow. He found refuge in Wakanda, rescued Hawkeye and Winter Soldier from Hydra, and later surrendered under Fisk's Super Hero Ban.",
  ["wiki-2099", "wiki-s0", "wiki-cap-lore", "wiki-s7"], aliases=["Steve Rogers"])
E("cloak-and-dagger", "Cloak & Dagger", "character", P,
  "A hero duo that the Entanglement fused so that only one of them can be physically present at a time. A portable TRD split them briefly, but Cloak teleported to save Dagger and joined them again.",
  ["wiki-present", "wiki-s1"])
E("cyclops", "Cyclops", "character", P,
  "Scott Summers, who was at Gambit and Rogue's wedding when Krakoa went to 2099. Alchemax captured him and used his optic blasts to make Punch Chronovium until Jean Grey freed him.",
  ["wiki-present", "wiki-s8"], aliases=["Scott Summers"])
E("daredevil", "Daredevil", "character", CO,
  "Matt Murdock of the Collapsed Timeline, who lost nearly everyone to the Hand. He took the demon Beast's power in Hell, became Yinglong's champion and led the Eighth City, then lost the Shenloong final to Lin Lie.",
  ["wiki-collapsed", "wiki-s4"], aliases=["Matt Murdock", "Dizang"])
E("deadpool", "Deadpool", "character", P,
  "Wade Wilson, who toured universes in a bus stolen from Doctor Strange and then worked for the Collector, taking beings from dying worlds. He turned on the Collector at the Museum and founded a Monster Kingdom at home.",
  ["wiki-s6", "wiki-present", "wiki-misc"], aliases=["Wade Wilson"])
E("devil-dinosaur", "Devil Dinosaur", "character", P,
  "Moon Girl's dinosaur partner, whom the Entanglement split from her and locked in the Collector's Museum. After his rescue he wore Chrono-Armor to lead the assault on Alchemax Headquarters.",
  ["wiki-present", "wiki-s8", "wiki-s6"])
E("doctor-strange", "Doctor Strange", "character", P,
  "The Sorcerer Supreme, who refused to give Doctor Doom the Darkhold and hid it in the Astral Plane, where he was then trapped. He won the book back from Khonshu, but its pages scattered as he escaped.",
  ["wiki-present", "wiki-s0", "wiki-s1"], aliases=["Stephen Strange"])
E("elsa-bloodstone", "Elsa Bloodstone", "character", CO,
  "A monster hunter from the Collapsed Timeline who lived in Bloodstone Manor with her brother Cullen. The Collector hired her to catch monsters, but she came to doubt the job and helped free the Museum's creatures.",
  ["wiki-collapsed", "wiki-s6"])
E("emma-frost", "Emma Frost", "character", P,
  "A Krakoan mutant leader who threw the 2099 Hellfire Gala and made a secret pact with Doom 2099 to drain Krakoa's chronal poison. Her Hellfire Protocol pushed Alchemax out of its markets.",
  ["wiki-s2", "wiki-s8", "wiki-present"])
E("gambit", "Gambit", "character", P,
  "Remy, whose wedding to Rogue was cut short when Krakoa was swept to 2099. He took the Grandmaster's deal to steal a von Doom contract from the Collector, and later died in Thebes and was revived.",
  ["wiki-s5", "wiki-s9", "wiki-present"], aliases=["Remy"])
E("gorr", "Gorr", "character", CO,
  "The God Butcher, a grieving believer who took up the Necrosword All-Black and spent centuries killing gods. He built a Godbomb to end all gods and died setting it off, after which he became the new King in Black.",
  ["wiki-gorr", "wiki-s10", "wiki-collapsed"], aliases=["God Butcher"])
E("groot", "Groot", "character", MO,
  "A Guardian of the Galaxy who crashed on Klyntar with his team. He later competed in the Shenloong Tournament and lost to a riddle he could not answer aloud.",
  ["wiki-mosaic", "wiki-s3", "wiki-s4"])
E("hawkeye", "Hawkeye", "character", P,
  "Clint Barton, sent by S.H.I.E.L.D. to rescue Winter Soldier from Hydra's Charteris Base. He cut off Bucky's tentacle arm to close the portal and escaped with Captain America to Wakanda.",
  ["wiki-s0", "wiki-present"], aliases=["Clint Barton"])
E("hela", "Hela", "character", P,
  "The Asgardian goddess of death, who found Chronovium in Hel and helped Loki seize Yggsgard. She later became Knull's Queen in Black, fled after Blade beat her, and asked for sanctuary in the Eighth City.",
  ["wiki-s0", "wiki-s3", "wiki-present"])
E("hulk", "Hulk", "character", CO,
  "Bruce Banner of the Collapsed Timeline, who built a Gamma Belt to control his changes. When the Entanglement turned his missile base into a demonic battleground, he became guardian of the Green Door and sent the banished Thor to Bloodstone Manor.",
  ["wiki-collapsed", "wiki-hulk-lore"], aliases=["Bruce Banner"])
E("human-torch", "Human Torch", "character", P,
  "Johnny of the Fantastic Four, who burned vampires on patrol during the Eternal Night. He planned to go supernova as a diversion so the heroes could reach Dracula's castle.",
  ["wiki-s1", "wiki-present"], aliases=["Johnny"])
E("invisible-woman", "Invisible Woman", "character", P,
  "Sue of the Fantastic Four, who scouted Dracula's army in Central Park. She rescued H.E.R.B.I.E. at Grand Central with help from Peni Parker's Spider-Bots.",
  ["wiki-s1", "wiki-present"], aliases=["Sue"])
E("iron-fist", "Iron Fist", "character", P,
  "Lin Lie, a former Sword Master who received Shou-Lao's chi after a near-fatal battle. When K'un-Lun fused with the other Capital Cities he was the only Immortal Weapon left, and he won the Shenloong Tournament.",
  ["wiki-ironfist-lore", "wiki-s4", "wiki-present"], aliases=["Lin Lie"])
E("iron-man", "Iron Man", "character", P,
  "Tony Stark, co-designer of the Timestream Reintegration Device, which he nicknamed Trudy. He rebooted Ultron's old body with a firewall to turn it against X-Tron.",
  ["wiki-trd", "wiki-s1", "wiki-s2"], aliases=["Tony Stark"])
E("jeff-the-land-shark", "Jeff the Land Shark", "character", "jeff-timeline",
  "A small land shark that Deadpool took for the Collector, who later wiped his memory. Jeff escaped the Museum, broke Knull's hold on the Guardians by humming, and swallowed the Norn Stone.",
  ["wiki-misc", "wiki-s3", "wiki-s6", "wiki-blood-hunt"], aliases=["Jeff"])
E("jubilee", "Jubilee", "character", P,
  "A mutant whose son Shogo was left stuck in dragon form by the Entanglement. She became Apocalypse's Horseman of Famine for his promise to cure Shogo, saw him murdered, and used his Death Seeds to revive fallen heroes.",
  ["wiki-s9", "wiki-present", "wiki-collapsed"], aliases=["Jubilation"])
E("loki", "Loki", "character", P,
  "The God of Mischief, who used visions from Chronovium-infused sap to seize Yggsgard and banish Thor. He later killed Psylocke in Thebes, was killed by Gorr, wrote his own fate on the Canvas of Destiny and returned.",
  ["wiki-s0", "wiki-s4", "wiki-s9", "wiki-s10"])
E("luna-snow", "Luna Snow", "character", P,
  "A Korean pop star and Tiger Division member whose Jeju Island concert Namor interrupted. Fisk jailed her in the Vault, and White Fox helped her escape.",
  ["wiki-present", "wiki-s7"])
E("magik", "Magik", "character", CO,
  "Illyana Rasputin, who became Queen of Limbo after her timeline's New Mutants died. She joined Scarlet Witch and Wolverine on a trip to Krakoa and later returned Angela to her home timeline.",
  ["wiki-s0", "wiki-collapsed", "wiki-s4"], aliases=["Illyana Rasputin"])
E("magneto", "Magneto", "character", P,
  "The leader of mutantkind on Krakoa, glad to find his people in 2099. He made a chaos-powered Cerebro with Scarlet Witch, was killed by Ultron and resurrected, and tore Cerebro from X-Tron.",
  ["wiki-s0", "wiki-s2", "wiki-present"])
E("mantis", "Mantis", "character", MO,
  "A Guardian of the Galaxy whom the Entanglement dropped into the Collector's Museum. She restored the Grand Garden with Loki, and later used his horn to find the Chronicler and get Thor brought back.",
  ["wiki-mosaic", "wiki-s6", "wiki-s10"])
E("mister-fantastic", "Mister Fantastic", "character", P,
  "Reed Richards, who works with the Mosaic Timeline's Shuri and with Tony Stark on the Timestream Reintegration Device. He named Chronovium as the key power source and led the Fantastic Four through the Eternal Night.",
  ["wiki-mrf-lore", "wiki-trd", "wiki-s1"], aliases=["Reed Richards"])
E("moon-knight", "Moon Knight", "character", P,
  "Marc Spector, Fist of Khonshu, who formed the Eternity Knights against Dracula's vampires. In Thebes he exposed Khonshu's massacres, and with the Eternity Mask he pushed back Gorr's Necroverse.",
  ["wiki-s0", "wiki-s1", "wiki-s9", "wiki-s10"], aliases=["Marc Spector"])
E("namor", "Namor", "character", P,
  "The king of Talokan, who went through a Krakoan gateway to talk alliance with Magneto. The talks failed, and he went home to attack Jeju Island.",
  ["wiki-present", "wiki-s2"])
E("peni-parker", "Peni Parker", "character", T99,
  "A pilot from Tokyo 2099 who guards the Master Weaver and Spider-Zero against Doom 2099's Doombots. She also studies Chronovium.",
  ["wiki-2099", "wiki-s0"])
E("phoenix", "Phoenix", "character", P,
  "Jean Grey, whose psychic link to Cyclops was cut by the Entanglement. As host of the Phoenix Force she cleansed Bast and fought Knull and Hela on Klyntar, then became the White Phoenix after absorbing Cyclops' energy.",
  ["wiki-s3", "wiki-s8", "wiki-present"], aliases=["Jean Grey"])
E("psylocke", "Psylocke", "character", "watercolor",
  "Sai, a psychic ninja from the destroyed Watercolor Timeline, whom Deadpool took for the Collector. She escaped and joined the X-Men, and in Thebes Loki killed her for her paint-like blood before a Death Seed revived her.",
  ["wiki-watercolor", "wiki-s9", "wiki-s6"], aliases=["Sai"])
E("rocket-raccoon", "Rocket Raccoon", "character", MO,
  "The Guardians' engineer, who swapped the Milano with a Celestial husk on Klyntar and planned the swap that sent Knull into the White Hot Room. A symbiote that healed him carried traces of his lost friend Lylla.",
  ["wiki-s3", "wiki-mosaic"], aliases=["Rocket"])
E("rogue", "Rogue", "character", P,
  "Gambit's bride, whose wedding on Krakoa was cut short by the timestorm. She absorbed Chronovium energy in the Grand Garden, and when she touched Doom 2099 she found that he had no memories at all.",
  ["wiki-s5", "wiki-s6", "wiki-present"])
E("scarlet-witch", "Scarlet Witch", "character", CO,
  "Wanda Maximoff of the Collapsed Timeline, who became Sorcerer Supreme after that reality's Doctor Strange died. She held her reality together, helped Strange from the Astral Plane and made an enhanced Cerebro with Magneto.",
  ["wiki-collapsed", "wiki-s0", "wiki-s3"], aliases=["Wanda Maximoff"])
E("spider-man", "Spider-Man", "character", P,
  "Peter Parker of the Present Timeline, recruited by Spider-Zero into the Web-Warriors. He freed heroes from the Vault, and at the God Quarry the God Tempest found him worthy of Mjolnir's power.",
  ["wiki-s0", "wiki-s7", "wiki-s10", "wiki-present"], aliases=["Peter Parker"])
E("squirrel-girl", "Squirrel Girl", "character", P,
  "A defender of New York during the Eternal Night who tried to save Ratatoskr from Dracula. On holiday on Krakoa she helped revive Psylocke's dying wolf.",
  ["wiki-s1", "wiki-s2", "wiki-present"], aliases=[])
E("star-lord", "Star-Lord", "character", MO,
  "Peter Quill, leader of the Guardians of the Galaxy, who led Shuri's scouting mission to Klyntar. The Milano crashed in a ship graveyard full of hungry symbiotes.",
  ["wiki-starlord-lore", "wiki-mosaic"], aliases=["Peter Quill"])
E("storm", "Storm", "character", P,
  "Ororo, who steered the islands Krakoa and Arakko through the Entanglement's timestorm and into 2099. At the God Quarry she accepted Eternity's power and became the Eternal Storm.",
  ["wiki-s0", "wiki-s10", "wiki-present"], aliases=["Ororo", "Eternal Storm"])
E("the-hood", "The Hood", "character", P,
  "Parker Robbins, a Vault inmate who escaped with the cloak of the entity Oblivion. Sent to take the Tablet of Death and Entropy from Apocalypse, he killed Ozymandias and Gambit in Thebes.",
  ["wiki-s9", "wiki-s7", "wiki-present"], aliases=["Parker Robbins"])
E("the-punisher", "The Punisher", "character", T99,
  "Frank Castle, kept alive into 2099 by a knock-off super-soldier serum. He joined Black Widow's Resistance, rode Devil Dinosaur into Alchemax HQ and used the TRD to send the building back to 2099.",
  ["wiki-2099", "wiki-s0", "wiki-s8"], aliases=["Frank Castle"])
E("the-thing", "The Thing", "character", P,
  "Ben Grimm of the Fantastic Four, who found the pure Chronovium crystal the TRD needed. On Yancy Street he found the vampire Black Panther and urged him to eat the Heart-Shaped Herb.",
  ["wiki-s1", "wiki-present"], aliases=["Ben Grimm"])
E("thor", "Thor", "character", P,
  "The God of Thunder, whom Loki banished to the Collapsed Timeline. He fought Gorr after Loki's death and gave his life to contain the Godbomb, then was restored when the Chronicler rearranged his own record of events.",
  ["wiki-s0", "wiki-collapsed", "wiki-s10"])
E("ultron", "Ultron", "character", T99,
  "An AI banished from Earth who returned after seventy years in space because Doom 2099 was trying to erase him from history. After his Hellfire Gala attack, Tony Stark rebooted his old body under a firewall to fight X-Tron.",
  ["wiki-2099", "wiki-s2"])
E("venom", "Venom", "character", "venom-timeline",
  "Eddie Brock and his symbiote, from a reality ravaged by Knull. They fought in the Collapsed Timeline's war with Magik, then on Klyntar took a Phoenix Egg shard and faced Knull with the Sword of Dracula.",
  ["wiki-misc", "wiki-venom-lore", "wiki-s3"], aliases=["Eddie Brock"])
E("white-fox", "White Fox", "character", P,
  "The director of Korea's Tiger Division, who warns that travel between timelines speeds up the Entanglement. She gave Lin Lie the last shard of the Sword of Fu Xi and helped Luna Snow escape the Vault.",
  ["wiki-whitefox", "wiki-s7", "wiki-present"])
E("winter-soldier", "Winter Soldier", "character", P,
  "Bucky Barnes, captured by Hydra's Occult Ops, who fused a tentacled arm onto him. He escaped to Wakanda with Hawkeye and Captain America, and in Thebes he confessed that he had once killed Wolverine's family.",
  ["wiki-s0", "wiki-s9", "wiki-present"], aliases=["Bucky Barnes"])
E("wolverine", "Wolverine", "character", P,
  "Logan, a Krakoan mutant with ties to the 2099 Resistance, who healed Captain America with Krakoan flowers and brought him to Wakanda. He was killed in Thebes and revived with a Death Seed.",
  ["wiki-s0", "wiki-s9", "wiki-present"], aliases=["Logan"])

# --- key NPCs and variants
E("victor-von-doom", "Doctor Doom", "character", P,
  "Victor von Doom, the present-day monarch of Latveria, whose time experiment set off the Timestream Entanglement together with his 2099 self. He works from the shadows, gathering Pure Blood Chronovium, Shou-Lao's chi and the Tablet of Life and Time.",
  ["wiki-doom", "wiki-s0", "wiki-s1", "wiki-heroes"], aliases=["Victor von Doom", "Doom"])
E("doom-2099", "Doom 2099", "character", T99,
  "The 2099 variant of Victor von Doom, who took part in the twin experiment that caused the Entanglement and named the resulting realities Chronoverses. He gave up his memories for power and now hunts the contract for his mother Cynthia's soul.",
  ["wiki-doom2099", "wiki-s0", "wiki-s5", "wiki-s6"], var="victor-von-doom", aliases=["Victor von Doom"])
E("galacta", "Galacta", "character", BY,
  "The daughter of Galactus and the game's announcer. She eats Chronovium instead of worlds and used her power to shield a handful of timelines so that the heroes could find a solution.",
  ["wiki-galacta", "wiki-s0"], aliases=["Gali", "Daughter of the Devourer"])
E("galactus", "Galactus", "character", BY,
  "The Devourer of Worlds and Galacta's father, who advised her to consume all of existence instead of preserving timelines.",
  ["wiki-galacta"])
E("dracula", "Dracula", "character", P,
  "The Lord of Vampires, who used a Chronovium shard from Doctor Doom and a drop of his own blood to lock New York in endless night. He escaped Fisk's Vault and returned during the Blood Hunt before Blade turned him to stone.",
  ["wiki-s1", "wiki-blood-hunt", "official-home"], aliases=["Vlad Dracula"])
E("knull", "Knull", "character", MO,
  "The King in Black, a dark god imprisoned in the core of Klyntar until the Entanglement woke him. He corrupted gods such as Bast and was finally destroyed when Rocket's device swapped him into the White Hot Room.",
  ["wiki-s3", "wiki-mosaic", "official-home"], aliases=["King in Black"])
E("master-weaver", "Master Weaver", "character", T99,
  "The keeper of the Web of Life and Destiny, based in the Spider-Islands above Tokyo 2099. He wants to use the temporal rift's energy to power the Web despite the danger to civilians.",
  ["wiki-2099", "wiki-s0", "official-home"])
E("spider-zero", "Spider-Zero", "character", T99,
  "The Master Weaver's apprentice, from a destroyed universe. Banished for opposing his plan, she gathered spider-people from other realities into the Web-Warriors, and later opened the portal that carried Knowhere to the God Quarry.",
  ["wiki-2099", "wiki-s0", "wiki-s10"])
E("shuri", "Shuri", "character", MO,
  "Princess of the Intergalactic Empire of Wakanda and the driving force of its science. She first contacted Reed Richards across realities, calls the fractured realities Chronoverses, and sent the Guardians to Klyntar.",
  ["wiki-mosaic", "wiki-mrf-lore", "wiki-s3"])
E("bast", "Bast", "character", MO,
  "The Panther Goddess of Wakanda's Orisha. Knull corrupted her until the Phoenix cleansed her in the Divine Space, after which she sent Shuri to gather warriors against Knull.",
  ["wiki-mosaic", "wiki-s3"])
E("khonshu", "Khonshu", "character", P,
  "The Egyptian moon god and Moon Knight's master, who merged with his variants after the Entanglement. In Thebes he caused massacres to turn faith into hatred and set Gorr on Apocalypse, and he died after Moon Knight beat back the Necroverse.",
  ["wiki-s0", "wiki-s9", "wiki-s10"])
E("apocalypse", "Apocalypse", "character", CO,
  "En Sabah Nur, who rebuilt Luxor in the Collapsed Timeline as Thebes and planned to absorb the faith of every god through his Faith-Harvesting Engine. He was murdered with All-Black on the day of his ascension.",
  ["wiki-collapsed", "wiki-s9"], aliases=["En Sabah Nur"])
E("kingpin", "Kingpin", "character", P,
  "Wilson Fisk, elected mayor of New York after the Eternal Night. He imposed a Super Hero Ban, bargained with the Gilded Saint, and resigned in shame after the heroes defeated him in Times Square.",
  ["wiki-s7", "wiki-blood-hunt"], aliases=["Wilson Fisk"])
E("the-collector", "The Collector", "character", BY,
  "An Elder of the Universe who gathers beings from dying universes for his Museum of Contemplation. He held the contract for Cynthia von Doom's soul, which he got from Mephisto.",
  ["wiki-s5", "wiki-s6"], aliases=[])
E("grandmaster", "Grandmaster", "character", BY,
  "En Dwi Gast, an Elder of the Universe who co-created the Grand Garden with the Gardener. He hired Gambit to steal the von Doom contract from the Collector.",
  ["wiki-s5", "wiki-s4"], aliases=["En Dwi Gast"])
E("tyler-stone", "Tyler Stone", "character", T99,
  "An Alchemax executive who answered the Hellfire Trading Company by moving the corporation's headquarters into the past. He supplied Doom 2099 with Punch Chronovium in exchange for help against the mutants.",
  ["wiki-2099", "wiki-s8"])
E("moon-girl", "Moon Girl", "character", P,
  "Lunella, separated from Devil Dinosaur by the Entanglement and caught by Alchemax in 2099. She was forced to study Punch Chronovium and triggered the incursion into the present, then helped the heroes undo it.",
  ["wiki-moongirl", "wiki-s8", "wiki-s10"], aliases=["Lunella"])
E("shou-lao", "Shou-Lao", "character", P,
  "The immortal dragon guardian of K'un-Lun and source of every Iron Fist's chi. The Entanglement froze him in a deep slumber until the heroes woke him, and he then hosted the Shenloong Tournament.",
  ["wiki-s4", "official-home", "wiki-te"], aliases=["Shou-Lao the Undying"])
E("yinglong", "Yinglong", "character", CO,
  "A divine spirit imprisoned by the Beast. Freed by Daredevil, it made him its champion in exchange for help to recover the Sword of Fu Xi and free the war god Chiyou.",
  ["wiki-s4"])
E("ratatoskr", "Ratatoskr", "character", P,
  "The giant Asgardian messenger squirrel whose horn can end an immortal's life. Dracula captured her during the Eternal Night and later turned her into a vampire with the Norn Stone.",
  ["wiki-s0", "wiki-s1", "wiki-blood-hunt"])
E("x-tron", "X-Tron", "character", T99,
  "A new body Ultron grew by hacking Krakoa's Resurrection Protocols, which gave it Krakoa's absorbed chronal energy. After Magneto took back Cerebro, Doom 2099 erased it from existence.",
  ["wiki-s2", "wiki-seasons"], var="ultron")
E("captain-america-present", "Captain America (Present Timeline)", "character", P,
  "The Present Timeline's Steve Rogers, who died saving Spider-Man from a gang of villains led by the Green Goblin. His spirit later appeared in Spider-Man's vision of worthiness at the God Quarry.",
  ["wiki-present", "wiki-s7", "wiki-s10"], var="captain-america")
E("doctor-strange-collapsed", "Doctor Strange (Collapsed Timeline)", "character", CO,
  "The Collapsed Timeline's Doctor Strange, who died in the final battle of the First Demon War. His death led Wanda Maximoff to take up the role of Sorcerer Supreme.",
  ["wiki-collapsed"], var="doctor-strange")
E("scarlet-witch-zombies", "Queen of the Dead", "character", "marvel-zombies",
  "A zombified Scarlet Witch of the Marvel Zombies Timeline, driven mad by the Vision's death. She leads her forces on New York in search of the zombie symbiote K-44.",
  ["wiki-zombies"], var="scarlet-witch")
E("the-chronicler", "The Chronicler", "character", BY,
  "An aged form of Loki who, after his death at Gorr's hands, chose to record the histories of seven cosmos from the House of Ideas. By rearranging his own account he brought Thor back to life.",
  ["wiki-s10"], var="loki")
E("cynthia-von-doom", "Cynthia von Doom", "character", P,
  "Victor von Doom's late mother. The contract for her soul passed from Mephisto to the Collector, and Doom 2099's lost memories of her drive his hunt for it.",
  ["wiki-doom", "wiki-doom2099", "wiki-s6"])
E("laussa", "Laussa Odinsdottir", "character", P,
  "Angela's infant sister, taken by Hela's undead Valkyries and displaced to K'un-Lun by the Entanglement. Lin Lie cared for her there.",
  ["wiki-present", "wiki-s4"], aliases=["Laussa"])
E("shogo-lee", "Shogo Lee", "character", P,
  "Jubilee's son, stuck in his dragon form by the Timestream Entanglement and left in the care of the mutants on Krakoa.",
  ["wiki-present", "wiki-s9"])

# --- places
E("krakoa", "Krakoa", "place", T99,
  "The living island and mutant nation, originally from the Present Timeline, that a timestorm carried into the 2099 Timeline. It hosted the 2099 Hellfire Gala and is poisoned by the chronal energy it absorbed.",
  ["wiki-present", "wiki-s2", "official-home"])
E("arakko", "Arakko", "place", T99,
  "Krakoa's sister island, once part of the landmass Okkara. It was displaced into 2099 together with Krakoa, and Ultron's virus took it over.",
  ["official-home", "wiki-s2", "wiki-present"])
E("yggsgard", "Yggsgard", "place", P,
  "The new realm formed when the World Tree Yggdrasil overgrew Asgard in the wake of the Entanglement. Loki took its throne, and Gorr later shattered its Bifrost.",
  ["wiki-te", "official-home", "wiki-s10"])
E("klyntar", "Klyntar", "place", MO,
  "The symbiote planet that holds Knull's prison, littered with a dead Celestial's husk. The Guardians, Venom, Phoenix and many heroes fought Knull and Hela there.",
  ["official-home", "wiki-s3", "wiki-mosaic"])
E("intergalactic-empire-of-wakanda", "Intergalactic Empire of Wakanda", "place", MO,
  "A star-spanning Wakanda led by T'Challa and Shuri, which shelters heroes from other realities. The Entanglement caused anomalies there and began merging the spirit realm Djalia with the capital Birnin T'Challa.",
  ["wiki-te", "official-home", "wiki-mosaic"])
E("tokyo-2099", "Tokyo 2099", "place", T99,
  "The future Tokyo, where a huge temporal rift opened above the city. The Master Weaver's Spider-Islands float above it, and Alchemax and the Public Eye hold power in its streets.",
  ["official-home", "wiki-s0", "wiki-2099"])
E("hydra-charteris-base", "Hydra Charteris Base", "place", P,
  "Hydra's Antarctic base, where the group mines Chronovium for super-soldiers and hides a portal to an ancient Hive. Also called Erebus Base in the lore.",
  ["official-home", "wiki-s0"], aliases=["Hell's Heaven", "Erebus Base"])
E("kun-lun", "K'un-Lun", "place", CO,
  "The mystic city of the Iron Fist, which the Entanglement fused with the other Capital Cities of Heaven into the Heart of Heaven and displaced into the Collapsed Timeline.",
  ["wiki-te", "official-home", "wiki-s4"], aliases=["Heart of Heaven"])
E("eighth-city", "The Eighth City", "place", CO,
  "Once a prison for criminals and monsters, now a refuge for those cast out of heaven, led by Daredevil under the title Dizang. Hela fled there for sanctuary.",
  ["wiki-s3", "wiki-s4"])
E("empire-of-eternal-night", "Empire of Eternal Night", "place", P,
  "Manhattan under Dracula's endless night, with his castle in Central Park. The Sanctum Sanctorum and the Baxter Building served as the heroes' strongholds.",
  ["official-home", "wiki-s1", "wiki-te"])
E("museum-of-contemplation", "Museum of Contemplation", "place", BY,
  "The Collector's gallery of beings taken from dying universes, merged with the Grandmaster's Grand Garden after the Entanglement. Deadpool freed its exhibits.",
  ["official-home", "wiki-s5", "wiki-s6"], aliases=["Collector's Gallery"])
E("grand-garden", "Grand Garden", "place", BY,
  "A realm made by the Grandmaster and the Gardener, where Gambit and Rogue spent their honeymoon. It withered from Rogue's Chronovium surge until Mantis and Loki restored it.",
  ["official-home", "wiki-s5", "wiki-s6"])
E("thebes", "Thebes", "place", CO,
  "Apocalypse's capital in the Collapsed Timeline, made from Luxor. After his murder a storm sealed his pyramid, trapping heroes inside with the killer.",
  ["official-home", "wiki-collapsed", "wiki-s9"])
E("god-quarry", "God Quarry", "place", BY,
  "A realm of gods outside any timeline, where Gorr first found All-Black and where dead gods are entombed. He tried to detonate his Godbomb there.",
  ["wiki-s10"])
E("omnipotence-city", "Omnipotence City", "place", BY,
  "A gathering place of gods from every reality, which Gorr reached after the Entanglement, emptied of gods and turned into his mobile fortress.",
  ["wiki-s10"])
E("the-vault", "The Vault", "place", P,
  "The prison where Mayor Fisk held arrested heroes, villains and seized artifacts. Black Cat and Spider-Man staged a breakout that freed many prisoners, Dracula among them.",
  ["wiki-s7", "wiki-blood-hunt"])

# --- artifacts
E("chronovium", "Chronovium", "artifact", P,
  "Crystals of chronal energy formed as a byproduct of the Timestream Entanglement, with a different look in each reality. Galacta eats them, and the heroes need large amounts to power the Timestream Reintegration Device.",
  ["wiki-chronovium", "wiki-s0", "wiki-galacta"])
E("blood-chronovium", "Blood Chronovium", "artifact", P,
  "Chronovium that Dracula fed with his blood to create the Eternal Night. Doctor Doom later used Dracula's essence to turn it into Pure Blood Chronovium.",
  ["wiki-chronovium", "wiki-s1"], var="chronovium", aliases=["Pure Blood Chronovium"])
E("punch-chronovium", "Punch Chronovium", "artifact", T99,
  "Chronovium that Alchemax overcharged with Cyclops' optic blasts. It can break dimensional barriers, and it powered the incursion of Alchemax HQ into the present.",
  ["wiki-chronovium", "wiki-s8"], var="chronovium")
E("timestream-reintegration-device", "Timestream Reintegration Device", "artifact", P,
  "A machine designed by Reed Richards, Tony Stark, Shuri and other geniuses to restore damaged realities. A full version needs vast chronal power, but portable prototypes can rewind damage and states.",
  ["wiki-trd", "wiki-s1", "wiki-s8"], aliases=["TRD", "Trudy"])
E("darkhold", "Darkhold", "artifact", P,
  "The book of sins that holds the Vampiric Verses and the Montesi Formula. Doom wanted it to study time, and its pages scattered when Strange escaped the Astral Plane.",
  ["wiki-s0", "wiki-s1"])
E("cerebro", "Cerebro", "artifact", T99,
  "The mutant device that stores minds for Krakoa's Resurrection Protocols. Magneto and Scarlet Witch rebuilt it with chaos magic to call mutants from many realities, and Ultron stole it.",
  ["wiki-s0", "wiki-s2"])
E("tablet-of-life-and-time", "Tablet of Life and Time", "artifact", P,
  "A relic kept in the Sanctum Sanctorum. The Gilded Saint and Fisk wanted it, but Black Cat gave it to Doctor Doom.",
  ["wiki-s7", "wiki-doom"])
E("tablet-of-death-and-entropy", "Tablet of Death and Entropy", "artifact", CO,
  "The counterpart of the Tablet of Life and Time, kept by Apocalypse, which can speak with the dead. The Hood seized it, and Doom 2099 snatched it from him.",
  ["wiki-s9"])
E("all-black", "All-Black", "artifact", MO,
  "Knull's living Necrosword, which can kill gods and drain souls. It drifted to the God Quarry, chose Gorr, and was destroyed with him when it set off the Godbomb.",
  ["wiki-s3", "wiki-s9", "wiki-s10"], aliases=["Necrosword"])
E("faith-harvesting-engine", "Faith-Harvesting Engine", "artifact", CO,
  "A Celestial artifact made by Apocalypse to drain the faith of every god. Khonshu absorbed its power, and Gorr took it to build his Godbomb.",
  ["wiki-s9", "wiki-s10"])
E("mjolnir", "Mjolnir", "artifact", P,
  "Thor's hammer, which held the God Tempest. Gorr shattered it and caged the Tempest for his Godbomb, and Spider-Man was later judged worthy of its power.",
  ["wiki-s10", "wiki-s0"])
E("sword-of-fu-xi", "Sword of Fu Xi", "artifact", P,
  "Lin Lie's divine sword, which shattered in battle and lodged in his arms. Daredevil needed it to free Chiyou, and White Fox later gave Lin Lie its final fragment.",
  ["wiki-ironfist-lore", "wiki-s4", "wiki-s7"])
E("eternity-mask", "Eternity Mask", "artifact", P,
  "A mask from Kingpin's vault that matches its wearer's strength to the opponent's. Doctor Doom gave it to Moon Knight in the God Quarry.",
  ["wiki-s7", "wiki-s10"])
E("norn-stone", "Norn Stone", "artifact", P,
  "An Asgardian reality-altering stone that Dracula stole from the Vault to restore his power. Blade cut it from him, and Jeff swallowed it.",
  ["wiki-blood-hunt"])
E("doom-contract", "Contract for Cynthia von Doom's Soul", "artifact", BY,
  "A deal for the soul of Doom's mother, which Mephisto traded to the Collector. Gambit and Rogue stole it, and Doom 2099 took it from Rogue on Krakoa.",
  ["wiki-s5", "wiki-s6", "wiki-doom2099"])
E("heart-shaped-herb", "Heart-Shaped Herb", "artifact", MO,
  "Wakanda's sacred herb, normally reserved for the Black Panther. It can cure vampirism, and Shuri gave Blade an experimental serum made from it.",
  ["wiki-s1", "wiki-s3", "wiki-galacta"])

# --- organizations and factions
E("fantastic-four", "Fantastic Four", "organization", P,
  "Reed Richards, Sue, Johnny and Ben Grimm, who defended New York during the Eternal Night and work on the TRD from the Baxter Building.",
  ["wiki-s1", "wiki-te"])
E("x-men", "X-Men", "organization", P,
  "The mutant heroes based on Krakoa, now in 2099. They fought Ultron at the Hellfire Gala, raided Alchemax HQ and investigated Apocalypse's murder.",
  ["wiki-s2", "wiki-s8", "wiki-s9"])
E("quiet-council", "Quiet Council", "organization", T99,
  "Krakoa's ruling council. Emma Frost's deal with Doom 2099 was kept from it because the council would not approve.",
  ["wiki-s2", "official-home"])
E("guardians-of-the-galaxy", "Guardians of the Galaxy", "organization", MO,
  "The Mosaic Timeline's spacefaring team of Star-Lord, Rocket, Groot and Mantis, sent by Shuri to Klyntar.",
  ["wiki-mosaic", "wiki-s3"])
E("web-warriors", "Web-Warriors", "organization", T99,
  "A team of spider-heroes from many realities that Spider-Zero gathered in Tokyo 2099 to stop the Master Weaver and protect the Web of Life and Destiny.",
  ["wiki-s0"])
E("resistance-2099", "The Resistance", "organization", T99,
  "Black Widow's opposition movement in 2099, with Wolverine and The Punisher among its allies. It followed Alchemax into the present to stop it from exploiting another reality.",
  ["wiki-s0", "wiki-s8"])
E("hydra", "Hydra", "organization", P,
  "A terrorist group that mines Chronovium at Charteris Base. Its Occult Ops division experiments on super-soldiers and serves an ancient Hive beyond a portal.",
  ["wiki-s0", "official-home"])
E("alchemax", "Alchemax", "organization", T99,
  "The megacorporation that dominates 2099. It captured Cyclops and Moon Girl, made Punch Chronovium and moved its headquarters into present-day Manhattan.",
  ["wiki-2099", "wiki-s8", "wiki-s7"])
E("tiger-division", "Tiger Division", "organization", P,
  "A Korean hero agency directed by White Fox. It set up a secret base at Empire State University to rescue heroes from the Vault.",
  ["wiki-s7"])
E("thieves-guild", "Thieves Guild", "organization", P,
  "New York's guild of thieves, once controlled by the Gilded Saint and freed by Black Cat's deal with Doom. Black Cat then became its Guildmaster.",
  ["wiki-s7", "wiki-s9"])
E("clan-akkaba", "Clan Akkaba", "organization", CO,
  "Apocalypse's followers in the Collapsed Timeline, which he rallied across Egypt. Ozymandias was one of its first members.",
  ["wiki-collapsed", "wiki-s9"])
E("horsemen-of-death", "Horsemen of Death", "organization", CO,
  "Apocalypse's four horsemen in the Collapsed Timeline, with Jubilee as the Horseman of Famine. After his death they sided with Moon Knight against Khonshu.",
  ["wiki-s8", "wiki-s9"])
E("eternity-knights", "Eternity Knights", "organization", P,
  "An alliance that Moon Knight formed with Iron Man, Wolverine, Winter Soldier, Adam Warlock and Psylocke to slay Dracula's vampires.",
  ["wiki-s1"])
E("avengers", "Avengers", "organization", P,
  "Earth's Mightiest Heroes, whom Thor summoned against Gorr over New York. They were defeated, and Captain America's shield was shattered.",
  ["wiki-s10", "wiki-s2"])
E("corporate-raiders", "Corporate Raiders", "organization", T99,
  "Alchemax's strike force of clone super-enforcers made in the image of heroes such as Gambit, Rogue, Magik, Wolverine and Star-Lord.",
  ["wiki-s8"])
E("elders-of-the-universe", "Elders of the Universe", "organization", BY,
  "Ancient cosmic beings, among them the Collector, the Grandmaster and the Gardener, some of whom merged their domains after the Entanglement.",
  ["wiki-s5"])

# ---------------------------------------------------------------- events
events = []


def V(slug, tl, title, summary, label, key, era, imp, parts, srcs):
    events.append(dict(slug=slug, timeline=tl or "present", title=title, summary=summary, date_label=label,
                       sort_key=key, era=era, importance=imp,
                       participants=[{"entity": e, "role": r} for e, r in parts], sources=srcs))


PRE = "Before the Entanglement"
S0 = "Season 0: Dooms' Rise"
S1 = "Season 1: Eternal Night Falls"
S2 = "Season 2: Hellfire Gala"
S3 = "Season 3: The Abyss Awakens"
S4 = "Season 4: Heart of the Dragon"
S5 = "Season 5: Love is a Battlefield"
S6 = "Season 6: Night at the Museum"
S7 = "Season 7: The Hunt Is On"
S8 = "Season 8: Sins of Alchemax"
S9 = "Season 9: The Mystery of Thebes"
S10 = "Season 10: Butcher's Blasphemy"

V("gorr-becomes-god-butcher", CO, "Gorr becomes the God Butcher",
  "After losing his family, the devout Gorr met his gods and learned they had ignored his prayers. The Necrosword All-Black, adrift in the God Quarry, answered his wish for the power to kill gods, and he struck down the god who had begged him for help.",
  "Hundreds of years ago", 1700.0, PRE, 4, [("gorr", "instigator"), ("all-black", "ally")], ["wiki-s10", "wiki-gorr"])
V("captain-america-frozen", T99, "Captain America is frozen in ice",
  "During his last mission of World War II, Steve Rogers' plane crashed into the Arctic. In this reality he stayed frozen until Alchemax held him as a secret asset in 2099.",
  "World War II", 1945.0, PRE, 2, [("captain-america", "victim")], ["wiki-2099", "wiki-cap-lore"])
V("lin-lie-becomes-iron-fist", P, "Lin Lie becomes the Iron Fist",
  "Lin Lie, the Sword Master of the Agents of Atlas, was badly hurt by a kumiho and his Sword of Fu Xi shattered. Shou-Lao saved him by granting him his chi, which made him the new Iron Fist without the usual trial.",
  "Before the Entanglement", 2024.5, PRE, 3, [("iron-fist", "victim"), ("shou-lao", "ally"), ("sword-of-fu-xi", "witness")], ["wiki-ironfist-lore", "wiki-present", "wiki-s4"])
V("doom-demands-darkhold", P, "Doctor Doom demands the Darkhold",
  "Doom came to the Sanctum Sanctorum for the Darkhold's Vampiric Verses, which he believed could unlock time. Strange refused, the two dueled, and Strange hid the book in the Astral Plane.",
  "A few months before the Entanglement", 2024.8, PRE, 3, [("victor-von-doom", "instigator"), ("doctor-strange", "rival"), ("darkhold", "witness")], ["wiki-s0", "wiki-present"])
V("doom-visits-khonshu", P, "Doom asks Khonshu to hold the moon",
  "Doom entered Khonshu's Divine Space and asked the moon god to keep the moon over one city so he could study vampires. Khonshu refused and banished him, and later warned Doom of a coming darkness.",
  "Before the Entanglement", 2024.85, PRE, 2, [("victor-von-doom", "instigator"), ("khonshu", "rival"), ("moon-knight", "witness")], ["wiki-s0", "wiki-s10"])
V("timestream-entanglement", P, "The Timestream Entanglement",
  "Doctor Doom and Doom 2099 mastered time at the same moment from two points in reality, and the clash tore the multiverse apart. Realities collapsed or merged into the Chronoverses, and Chronovium crystals formed as a byproduct.",
  "Dooms' Rise", 2025.0, S0, 5, [("victor-von-doom", "instigator"), ("doom-2099", "instigator"), ("chronovium", "witness")], ["wiki-te", "wiki-s0", "wiki-chronoverses", "official-home"])
V("galacta-preserves-timelines", BY, "Galacta shields a handful of timelines",
  "Galacta found that Chronovium could satisfy her hunger but saw that the Entanglement could end every reality. She used her power to protect a few timelines so that their heroes could find a fix, and the effort left her too drained to fight.",
  "Dooms' Rise", 2025.005, S0, 3, [("galacta", "ally"), ("chronovium", "witness")], ["wiki-galacta", "wiki-s0"])
V("krakoa-carried-to-2099", T99, "Storm steers Krakoa into 2099",
  "A timestorm struck Arakko and Krakoa during the Entanglement. Storm calmed it and guided the sister islands through, but they came out in the year 2099, where Magneto welcomed a future of prosperity for mutantkind.",
  "2099 (Dooms' Rise)", 2025.01, S0, 4, [("storm", "instigator"), ("krakoa", "victim"), ("arakko", "victim"), ("magneto", "witness")], ["wiki-s0", "wiki-te", "wiki-present"])
V("loki-seizes-yggsgard", P, "Loki seizes Yggsgard and banishes Thor",
  "Chronovium-infused sap from the overgrown World Tree showed Loki a future in which he ruled. With Karnilla and Hela he put Odin into the Odinsleep, overpowered Thor and sent him through a portal into another timeline.",
  "Dooms' Rise", 2025.02, S0, 4, [("loki", "instigator"), ("hela", "ally"), ("thor", "victim"), ("yggsgard", "witness")], ["wiki-s0", "official-home"])
V("spider-zero-banished", T99, "The Master Weaver banishes Spider-Zero",
  "A huge temporal rift opened over Tokyo 2099, and the Master Weaver wanted to use its energy for the Web of Life and Destiny. Spider-Zero objected because of the danger to civilians and was banished from the Spider-Islands, so she began to gather the Web-Warriors.",
  "2099 (Dooms' Rise)", 2025.025, S0, 3, [("master-weaver", "instigator"), ("spider-zero", "victim"), ("web-warriors", "ally"), ("peni-parker", "ally"), ("spider-man", "ally")], ["wiki-s0", "official-home", "wiki-galacta"])
V("widow-frees-captain-america", T99, "Black Widow frees Captain America from Alchemax",
  "Following a tip about a guarded asset, Natalia Romanova broke into Alchemax and found Steve Rogers frozen. She woke him, and they fought the Public Eye before Wolverine healed Cap with Krakoan flowers and took him to Wakanda.",
  "2099 (Dooms' Rise)", 2025.03, S0, 3, [("black-widow", "instigator"), ("captain-america", "ally"), ("wolverine", "ally"), ("alchemax", "enemy")], ["wiki-s0", "wiki-2099"])
V("enhanced-cerebro", T99, "Magneto and Scarlet Witch forge an enhanced Cerebro",
  "Scarlet Witch, Magik and Wolverine reached Krakoa from the Collapsed Timeline. Wanda and Magneto built a version of Cerebro powered by chaos magic, which let them summon mutants from nearby realities to Krakoa.",
  "2099 (Dooms' Rise)", 2025.035, S0, 3, [("magneto", "instigator"), ("scarlet-witch", "ally"), ("magik", "ally"), ("wolverine", "ally"), ("cerebro", "witness")], ["wiki-s0"])
V("hydra-base-escape", P, "Escape from Hydra Charteris Base",
  "Winter Soldier was captured while spying on Hydra's base, and Hawkeye came to rescue him. To close the portal to Hydra's ancient creature, Hawkeye cut off Bucky's tentacled arm, and Captain America then led them through a portal to Wakanda.",
  "Dooms' Rise", 2025.04, S0, 3, [("winter-soldier", "victim"), ("hawkeye", "ally"), ("captain-america", "ally"), ("hydra", "enemy"), ("hydra-charteris-base", "witness"), ("shuri", "ally")], ["wiki-s0", "official-home"])
V("thor-at-bloodstone-manor", CO, "Thor recovers at Bloodstone Manor",
  "Banished into the Collapsed Timeline, Thor met Bruce Banner, who sent him to rest at Bloodstone Manor. There Thor cut Cullen Bloodstone's bond to the parasite Glartrox, which Elsa captured for her own use.",
  "After Thor's banishment", 2025.045, S0, 2, [("thor", "ally"), ("hulk", "ally"), ("elsa-bloodstone", "ally")], ["wiki-collapsed", "wiki-s6"])
V("first-klyntar-mission", MO, "The Guardians' first mission to Klyntar",
  "Shuri sent the Guardians to find the source of a spreading darkness, and the Milano crash-landed on Klyntar. With Venom they found the Codex of the dead Celestial and turned it into a bomb, but Knull survived.",
  "Dooms' Rise", 2025.05, S0, 3, [("guardians-of-the-galaxy", "ally"), ("star-lord", "ally"), ("venom", "ally"), ("knull", "enemy"), ("shuri", "instigator"), ("klyntar", "witness")], ["wiki-s3", "official-home", "wiki-starlord-lore"])
V("eternal-night-falls", P, "Dracula plunges New York into eternal night",
  "Doctor Doom gave Dracula a Chronovium shard and told him that a drop of his blood would let him control time over a city. Dracula stopped the moon over New York, and vampires took to the streets.",
  "Eternal Night Falls", 2025.10, S1, 4, [("dracula", "instigator"), ("victor-von-doom", "instigator"), ("blood-chronovium", "witness"), ("empire-of-eternal-night", "witness"), ("fantastic-four", "ally")], ["wiki-s1", "official-home", "wiki-doom"])
V("strange-wins-darkhold", P, "Strange wins the Darkhold from Khonshu",
  "Trapped in the Astral Plane, Strange found that Khonshu had the Darkhold and wanted to use the Montesi Formula to destroy all vampires, turned civilians included. Strange won the book and his freedom in a game, but its pages scattered as he escaped.",
  "Eternal Night Falls", 2025.11, S1, 3, [("doctor-strange", "instigator"), ("khonshu", "rival"), ("scarlet-witch", "ally"), ("darkhold", "witness")], ["wiki-s1", "wiki-s0"])
V("dracula-captures-blade", P, "Dracula captures Blade",
  "Spider-Man and Blade fought vampires in Central Park until Dracula himself defeated them and carried Blade away. Dracula drained him over and over to try to make his minions into Daywalkers.",
  "Eternal Night Falls", 2025.12, S1, 3, [("dracula", "instigator"), ("blade", "victim"), ("spider-man", "witness")], ["wiki-s1", "wiki-s3"])
V("black-panther-turned", P, "Black Panther becomes a vampire",
  "T'Challa came to New York with a Heart-Shaped Herb to help cure vampirism. Dracula's fangs could not pierce his armor, so Dracula used his Blood Chronovium instead, and T'Challa changed in body but resisted Dracula's control.",
  "Eternal Night Falls", 2025.13, S1, 3, [("black-panther", "victim"), ("dracula", "instigator"), ("heart-shaped-herb", "witness")], ["wiki-s1", "wiki-bp-lore"])
V("eternity-knights-formed", P, "Moon Knight forms the Eternity Knights",
  "Moon Knight formed an alliance with Iron Man, Wolverine, Winter Soldier, Adam Warlock and Psylocke to slay vampires, whether or not they had been civilians. They ran into a vampire faction led by Black Panther.",
  "Eternal Night Falls", 2025.14, S1, 2, [("moon-knight", "leader"), ("eternity-knights", "ally"), ("iron-man", "ally"), ("black-panther", "rival")], ["wiki-s1"])
V("dracula-defeated", P, "Dracula falls and Doom claims Pure Blood Chronovium",
  "The heroes freed Ratatoskr, who broke the barrier around Dracula's castle in Central Park, and they defeated Dracula. Doom had secretly helped them so that he could seize Dracula's essence as Pure Blood Chronovium.",
  "Eternal Night Falls", 2025.18, S1, 4, [("dracula", "victim"), ("victor-von-doom", "instigator"), ("ratatoskr", "ally"), ("human-torch", "ally"), ("invisible-woman", "ally"), ("blood-chronovium", "witness")], ["wiki-s1", "wiki-doom", "official-home"])
V("hellfire-gala-attack", T99, "Ultron crashes the Hellfire Gala",
  "Emma Frost threw a Hellfire Gala to reintroduce Krakoa, and Doom 2099 attended to reach the island's chronal energy. Ultron, back after seventy years in space, invaded through the Krakoan gateways and killed Magneto, who was resurrected.",
  "2099 (Hellfire Gala)", 2025.20, S2, 4, [("emma-frost", "instigator"), ("ultron", "enemy"), ("doom-2099", "witness"), ("magneto", "victim"), ("krakoa", "witness"), ("x-men", "ally")], ["wiki-s2", "official-home", "wiki-doom2099"])
V("x-tron-born", T99, "Ultron is reborn as X-Tron",
  "The heroes beat Ultron, but he had already hacked the Resurrection Protocols to grow a new body. As X-Tron he took Cerebro and fled to Arakko, while Tony Stark rebooted Ultron's old body behind a firewall.",
  "2099 (Hellfire Gala)", 2025.22, S2, 3, [("x-tron", "instigator"), ("ultron", "instigator"), ("iron-man", "ally"), ("cerebro", "witness"), ("arakko", "witness")], ["wiki-s2"])
V("doom-2099-erases-x-tron", T99, "Doom 2099 erases X-Tron",
  "Under a secret pact with Emma Frost, Doom 2099 drew the poisoning chronal energy out of Krakoa. After Magneto ripped Cerebro from X-Tron, Doom used that energy to erase X-Tron from existence, then turned on the heroes; the old Ultron stabbed him, but it was only a Doombot.",
  "2099 (Hellfire Gala)", 2025.26, S2, 4, [("doom-2099", "instigator"), ("x-tron", "victim"), ("emma-frost", "ally"), ("magneto", "ally"), ("ultron", "rival")], ["wiki-s2", "wiki-doom2099"])
V("hela-queen-in-black", MO, "Hela becomes the Queen in Black",
  "Angry that Loki had joined the heroes, Hela answered Knull's whispers and went to Klyntar. Knull made her his Queen in Black and gave her great power to guard the planet against the oncoming Phoenix.",
  "The Abyss Awakens", 2025.30, S3, 3, [("hela", "instigator"), ("knull", "ally"), ("klyntar", "witness")], ["wiki-s3"])
V("phoenix-purifies-bast", MO, "The Phoenix cleanses Bast",
  "Racing through the Divine Space toward Klyntar, the Phoenix met Bast and other gods that Knull had corrupted and burned the corruption out of them. Bast then sent Shuri to recruit warriors, starting with Blade.",
  "The Abyss Awakens", 2025.31, S3, 3, [("phoenix", "ally"), ("bast", "victim"), ("shuri", "ally"), ("blade", "ally")], ["wiki-s3"])
V("phoenix-egg-shatters", MO, "The Phoenix Egg shatters and Knull is freed",
  "Overwhelmed by Hela, the Phoenix sealed itself in an egg. A Celestial weapon that Tony Stark triggered by accident shattered the egg, which tore open Klyntar and freed Knull, while shards of the Phoenix Force bonded with several heroes.",
  "The Abyss Awakens", 2025.33, S3, 4, [("phoenix", "victim"), ("hela", "enemy"), ("iron-man", "witness"), ("knull", "instigator"), ("venom", "ally")], ["wiki-s3"])
V("knull-defeated", MO, "Knull is swapped into the White Hot Room",
  "After Venom failed to beat Knull with the Phoenix-charged Sword of Dracula, Rocket planned a quantum swap. Jean Grey let herself be struck down to be reborn in the White Hot Room, and Rocket's devices swapped her with Knull, who was destroyed.",
  "The Abyss Awakens", 2025.36, S3, 5, [("knull", "victim"), ("rocket-raccoon", "instigator"), ("phoenix", "ally"), ("venom", "ally"), ("scarlet-witch", "ally"), ("all-black", "witness")], ["wiki-s3", "wiki-s9"])
V("hela-flees-to-eighth-city", CO, "Hela seeks sanctuary in the Eighth City",
  "After Blade drained her blood and beat her, Hela feared Knull's revenge and fled. Dizang let her into the Eighth City but kept her sealed in a cell until she could be trusted.",
  "The Abyss Awakens", 2025.37, S3, 2, [("hela", "victim"), ("daredevil", "witness"), ("eighth-city", "witness"), ("blade", "enemy")], ["wiki-s3", "wiki-s4"])
V("doom-invades-kun-lun", CO, "Doom invades K'un-Lun for Shou-Lao's chi",
  "The Entanglement fused K'un-Lun with the other Capital Cities into the Heart of Heaven and froze Shou-Lao. While Lin Lie was away, Doom invaded to take the chronal-infused chi in the dragon's heart, and the heroes used an ancient rite to wake Shou-Lao.",
  "Heart of the Dragon", 2025.40, S4, 3, [("victor-von-doom", "instigator"), ("shou-lao", "victim"), ("iron-fist", "ally"), ("kun-lun", "witness")], ["wiki-s4", "official-home", "wiki-te"])
V("shenloong-tournament", CO, "The Shenloong Tournament",
  "Doom challenged Lin Lie's right to the title, and Shou-Lao invoked an old law that called a tournament of Immortal Weapons. In the final, Daredevil knocked the Fu Xi shards from Lin Lie's arms, but this unblocked his chi and he won as the true Iron Fist.",
  "Heart of the Dragon", 2025.45, S4, 4, [("iron-fist", "ally"), ("daredevil", "rival"), ("shou-lao", "witness"), ("loki", "rival"), ("grandmaster", "witness"), ("sword-of-fu-xi", "witness")], ["wiki-s4", "official-home"])
V("loki-steals-chi", CO, "Loki steals Shou-Lao's chi for Doom",
  "Loki hid cloaked during the Trial of Wisdom, then stabbed Shou-Lao's heart when Lin Lie hesitated to claim the prize. He moved the chi into Doom, and Doom paid him with a Phoenix Feather.",
  "Heart of the Dragon", 2025.47, S4, 4, [("loki", "instigator"), ("victor-von-doom", "ally"), ("shou-lao", "victim"), ("iron-fist", "witness")], ["wiki-s4", "wiki-doom"])
V("grandmaster-hires-gambit", BY, "The Grandmaster hires Gambit",
  "The Grandmaster saw a contract signed 'von Doom' in the Collector's Gallery and wanted it as a bargaining chip. He offered Gambit Chronovium wedding rings and a honeymoon in the Grand Garden if he stole it.",
  "Love is a Battlefield", 2025.50, S5, 3, [("grandmaster", "instigator"), ("gambit", "ally"), ("rogue", "witness"), ("doom-contract", "witness")], ["wiki-s5"])
V("doom-2099-seeks-cynthia", T99, "Doom 2099 hunts for the woman in his visions",
  "Doom 2099 had given up his early memories for power, but after the Entanglement he began to see a woman calling to him from a hellish realm. In a broken Chronovium shard he saw a contract bearing the name Cynthia and traced it to the Collector.",
  "2099 (Love is a Battlefield)", 2025.51, S5, 3, [("doom-2099", "instigator"), ("cynthia-von-doom", "victim"), ("the-collector", "witness")], ["wiki-s5", "wiki-doom2099"])
V("rogue-absorbs-chronovium", BY, "Rogue absorbs Chronovium and the heist goes wrong",
  "Gambit stole a fake contract while the Collector was distracted by a contest. Rogue touched his Chronovium die and absorbed its energy, which withered the Grand Garden and destroyed their way home, and it let them reach the real contract.",
  "Love is a Battlefield", 2025.53, S5, 3, [("rogue", "victim"), ("gambit", "instigator"), ("magneto", "witness"), ("the-collector", "enemy"), ("grand-garden", "witness")], ["wiki-s5"])
V("museum-breakout", BY, "Deadpool frees the Museum of Contemplation",
  "Ordered to capture Gambit and Rogue, Deadpool switched sides and smashed the display cases to free their prisoners. Elsa Bloodstone and Devil Dinosaur beat a Brood Queen, and the heroes escaped the Museum.",
  "Night at the Museum", 2025.55, S6, 3, [("deadpool", "instigator"), ("elsa-bloodstone", "ally"), ("devil-dinosaur", "ally"), ("the-collector", "enemy"), ("jeff-the-land-shark", "ally"), ("museum-of-contemplation", "witness")], ["wiki-s6", "official-home"])
V("grand-garden-restored", BY, "Mantis and Loki restore the Grand Garden",
  "An invisible barrier trapped the Guardians in the Grand Garden. Mantis and Loki combined healing and Asgardian magic to bring the garden back, so the Gardener let them go, but Loki secretly planted a sapling for his own ends.",
  "Night at the Museum", 2025.555, S6, 2, [("mantis", "ally"), ("loki", "ally"), ("guardians-of-the-galaxy", "witness"), ("grand-garden", "witness")], ["wiki-s6", "wiki-s10"])
V("gambit-rogue-wedding", T99, "Gambit and Rogue complete their wedding",
  "Once Rogue could control her new power, she was allowed back on Krakoa, and the couple finished their wedding. Emma Frost helped turn the Chronovium die into a new ring.",
  "2099 (Night at the Museum)", 2025.56, S6, 2, [("gambit", "ally"), ("rogue", "ally"), ("emma-frost", "ally"), ("krakoa", "witness")], ["wiki-s6"])
V("doom-2099-takes-contract", T99, "Doom 2099 takes the contract",
  "Doom 2099 broke into Rogue's room on Krakoa, disabled her powers and found the contract, then wept on reading Cynthia von Doom's name. When Rogue touched him she found no memories at all, and she passed out as he fled with it.",
  "2099 (Night at the Museum)", 2025.565, S6, 4, [("doom-2099", "instigator"), ("rogue", "victim"), ("doom-contract", "witness"), ("cynthia-von-doom", "witness")], ["wiki-s6", "wiki-doom2099"])
V("monster-kingdom-founded", P, "Deadpool founds his Monster Kingdom",
  "Elsa persuaded Deadpool to care for the creatures freed from the Collector. Magik and Scarlet Witch opened a portal to his home timeline, where he set up his Monster Kingdom.",
  "Night at the Museum", 2025.57, S6, 1, [("deadpool", "leader"), ("elsa-bloodstone", "ally"), ("magik", "ally"), ("scarlet-witch", "ally")], ["wiki-s6", "wiki-present"])
V("alchemax-captures-moon-girl", T99, "Alchemax captures Moon Girl and Cyclops",
  "The Entanglement threw Moon Girl into 2099, where Alchemax tracked her and Cyclops by their time signatures. Cyclops was forced to charge Chronovium with his optic blasts, and Moon Girl was made to study the resulting Punch Chronovium.",
  "2099 (Sins of Alchemax)", 2025.58, S8, 3, [("moon-girl", "victim"), ("cyclops", "victim"), ("alchemax", "instigator"), ("punch-chronovium", "witness")], ["wiki-s8", "wiki-moongirl"])
V("alchemax-incursion", P, "Alchemax HQ invades Lower Manhattan",
  "Tyler Stone planned to beat the mutants by selling future goods to the past. Moon Girl's activation of the crystal carried Alchemax HQ into present-day New York, and a chronal plague began turning Lower Manhattan into Nueva York.",
  "The Hunt Is On", 2025.60, S7, 4, [("alchemax", "instigator"), ("tyler-stone", "instigator"), ("moon-girl", "witness"), ("punch-chronovium", "witness")], ["wiki-s8", "wiki-s7", "official-home"])
V("super-hero-ban", P, "Mayor Fisk's Super Hero Ban",
  "Mayor Fisk locked down Lower Manhattan, banned vigilantes and held arrested heroes in the Vault. He also made a secret deal with the Gilded Saint to undo the chronal damage in exchange for the Tablet of Life and Time.",
  "The Hunt Is On", 2025.61, S7, 3, [("kingpin", "instigator"), ("captain-america", "victim"), ("luna-snow", "victim"), ("the-vault", "witness"), ("tiger-division", "enemy")], ["wiki-s7"])
V("vault-breakout", P, "The Vault breakout",
  "Black Cat and Spider-Man used the delivery of the Tablet as a Trojan horse to break the captive heroes out of the Vault. Parker Robbins found the Cloak of Oblivion in the chaos, and Dracula also escaped.",
  "The Hunt Is On", 2025.63, S7, 3, [("black-cat", "instigator"), ("spider-man", "instigator"), ("captain-america", "ally"), ("the-hood", "witness"), ("dracula", "witness"), ("the-vault", "witness")], ["wiki-s7", "wiki-blood-hunt", "wiki-s9"])
V("doom-gets-tablet", P, "Black Cat trades the Tablet of Life and Time to Doom",
  "Black Cat gave Fisk a replica, swapped by Rocket's Nega-Energy Replicator, and kept the real Tablet. Doom offered her immortality for it, but she asked him to free the Thieves Guild from the Gilded Saint instead, and she became Guildmaster.",
  "The Hunt Is On", 2025.64, S7, 3, [("black-cat", "ally"), ("victor-von-doom", "instigator"), ("tablet-of-life-and-time", "witness"), ("thieves-guild", "witness"), ("rocket-raccoon", "ally")], ["wiki-s7", "wiki-doom"])
V("blood-hunt", P, "The Blood Hunt",
  "Dracula used a Norn Stone from the Vault to raise a new army and turned Ratatoskr into a vampire. A squad of Blade, Punisher, Thor, Squirrel Girl and Jeff hunted him down, and Blade cut out the stone, turning Dracula to stone.",
  "Blood Hunt (The Hunt Is On)", 2025.66, S7, 3, [("dracula", "instigator"), ("blade", "ally"), ("the-punisher", "ally"), ("thor", "ally"), ("squirrel-girl", "ally"), ("jeff-the-land-shark", "ally"), ("norn-stone", "witness")], ["wiki-blood-hunt"])
V("kingpin-ousted", P, "Kingpin is driven from office",
  "Fisk ambushed the tired heroes in Times Square after the Blood Hunt, and they defeated him in public. Shamed, he stepped down as mayor.",
  "Blood Hunt (The Hunt Is On)", 2025.67, S7, 2, [("kingpin", "victim"), ("blade", "enemy"), ("daredevil", "witness")], ["wiki-blood-hunt", "wiki-s7"])
V("doom-2099-alchemax-deal", T99, "Doom 2099 seals his deal with Alchemax",
  "Doom 2099 had given Alchemax Chronovium to study, and in return he crippled the Hellfire Trading Company by draining Krakoa. Tyler Stone handed him a Punch Chronovium crystal to close the deal.",
  "2099 (Sins of Alchemax)", 2025.70, S8, 3, [("doom-2099", "instigator"), ("tyler-stone", "ally"), ("punch-chronovium", "witness"), ("emma-frost", "enemy")], ["wiki-s8", "wiki-doom2099"])
V("white-phoenix", P, "Jean frees Cyclops and becomes the White Phoenix",
  "During the raid on Alchemax HQ, Jean Grey found Scott held in ruby quartz, unable to close his eyes. She absorbed his endless optic energy, which healed him and restored the weakened Phoenix Force as the White Phoenix.",
  "Sins of Alchemax", 2025.71, S8, 3, [("phoenix", "ally"), ("cyclops", "victim"), ("rogue", "ally"), ("alchemax", "enemy")], ["wiki-s8"])
V("alchemax-returned", P, "Alchemax HQ is sent back to 2099",
  "Devil Dinosaur in Chrono-Armor and the Punisher led the charge into Alchemax HQ, where they gave Moon Girl a miniature TRD. The Punisher stayed behind and used it to send the building, and himself, back to 2099.",
  "Sins of Alchemax", 2025.72, S8, 4, [("the-punisher", "instigator"), ("devil-dinosaur", "ally"), ("moon-girl", "ally"), ("deadpool", "ally"), ("timestream-reintegration-device", "witness"), ("alchemax", "victim")], ["wiki-s8", "official-home"])
V("jubilee-joins-apocalypse", CO, "Jubilee becomes the Horseman of Famine",
  "Searching for a cure for Shogo, Jubilee went to the Collapsed Timeline and met Apocalypse. He promised to restore her son if she served as his Horseman of Famine, and she gained power at the cost of a burning hunger.",
  "Sins of Alchemax", 2025.73, S8, 3, [("jubilee", "ally"), ("apocalypse", "instigator"), ("shogo-lee", "witness"), ("horsemen-of-death", "witness")], ["wiki-s9", "wiki-s8", "wiki-collapsed"])
V("apocalypse-murdered", CO, "Apocalypse is murdered",
  "On the day of his ascension through the Faith-Harvesting Engine, Apocalypse was impaled by a pitch-black sword. The Lazarus Chamber could not revive him, and a storm sealed his pyramid with the heroes and the killer inside.",
  "The Mystery of Thebes", 2025.80, S9, 5, [("apocalypse", "victim"), ("jubilee", "witness"), ("gorr", "instigator"), ("thebes", "witness"), ("faith-harvesting-engine", "witness")], ["wiki-s9", "official-home"])
V("thebes-investigation", CO, "Murders in the sealed pyramid",
  "Trapped heroes searched for the killer while new deaths struck: Winter Soldier's arm drained Wolverine, Loki killed Psylocke, and The Hood shot Gambit. Jubilee revived each with Death Seeds, and the clues pointed to All-Black and the God Butcher.",
  "The Mystery of Thebes", 2025.82, S9, 4, [("emma-frost", "leader"), ("daredevil", "ally"), ("wolverine", "victim"), ("psylocke", "victim"), ("gambit", "victim"), ("winter-soldier", "instigator"), ("loki", "instigator"), ("the-hood", "instigator"), ("jubilee", "ally")], ["wiki-s9"])
V("doom-2099-steals-tablet-of-death", P, "Doom 2099 snatches the Tablet of Death and Entropy",
  "The Hood gave the heroes the Tablet, then stole it back while Moon Knight's ritual raised crying spirits. Back in the Bronx, Doom 2099 stepped out of a portal and took it from him.",
  "The Mystery of Thebes", 2025.84, S9, 3, [("the-hood", "victim"), ("doom-2099", "instigator"), ("moon-knight", "witness"), ("tablet-of-death-and-entropy", "witness")], ["wiki-s9"])
V("khonshu-exposed", CO, "Moon Knight exposes Khonshu",
  "Moon Knight found that Khonshu had caused massacres so that his victims' hatred would flow to Apocalypse and draw Gorr to him. Confronted, Khonshu absorbed the Engine's unpurified faith, but Gorr broke into Thebes, impaled him and dragged him and the Engine away.",
  "The Mystery of Thebes", 2025.86, S9, 4, [("moon-knight", "instigator"), ("khonshu", "victim"), ("gorr", "enemy"), ("jubilee", "ally"), ("faith-harvesting-engine", "witness")], ["wiki-s9"])
V("gorr-attacks-yggsgard", P, "Gorr kills Loki and shatters Mjolnir",
  "Gorr destroyed the Bifrost and killed Loki with All-Black. The battle with Thor spread to New York, where the Avengers fell, Captain America's shield broke, and Gorr shattered Mjolnir to cage the God Tempest.",
  "Butcher's Blasphemy", 2025.90, S10, 5, [("gorr", "instigator"), ("loki", "victim"), ("thor", "victim"), ("spider-man", "ally"), ("captain-america", "victim"), ("avengers", "ally"), ("mjolnir", "victim"), ("yggsgard", "witness")], ["wiki-s10"])
V("loki-becomes-chronicler", BY, "Loki becomes the Chronicler",
  "Dying in the Void, Loki found the Ink of Destiny was his own blood and wrote his fate with the Phoenix quill. The Never Queen showed him that destiny cannot be forced, and he chose to record the past as the Chronicler.",
  "Butcher's Blasphemy", 2025.91, S10, 3, [("loki", "instigator"), ("the-chronicler", "witness")], ["wiki-s10"])
V("battle-of-god-quarry", BY, "The Battle of the God Quarry",
  "Spider-Zero opened a way for Knowhere into the God Quarry, where Gorr would set off his Godbomb. Moon Knight with the Eternity Mask, Storm empowered by Eternity, and Spider-Man worthy of the God Tempest fought Gorr, and Thor died containing the blast.",
  "Butcher's Blasphemy", 2025.95, S10, 5, [("gorr", "instigator"), ("thor", "victim"), ("moon-knight", "ally"), ("storm", "ally"), ("spider-man", "ally"), ("spider-zero", "ally"), ("victor-von-doom", "ally"), ("khonshu", "victim"), ("god-quarry", "witness"), ("all-black", "witness")], ["wiki-s10"])
V("gorr-king-in-black", MO, "Gorr becomes the King in Black",
  "Gorr's spirit reached the Un-Beyond, where the Eventuality offered him the role of King in Black to hold back darkness. With All-Black by his side, he took the role and went to Klyntar to hunt true cosmic evils.",
  "Butcher's Blasphemy", 2025.96, S10, 4, [("gorr", "instigator"), ("all-black", "ally"), ("klyntar", "witness")], ["wiki-s10"])
V("thor-restored", BY, "The Chronicler brings Thor back",
  "Mantis followed Loki's glowing horn to the House of Ideas, where the Chronicler kept his record. By moving one passage of the account, he brought Thor back to life, and a reborn Loki later appeared in Yggsgard.",
  "Butcher's Blasphemy", 2025.97, S10, 4, [("mantis", "instigator"), ("the-chronicler", "ally"), ("thor", "victim"), ("loki", "witness")], ["wiki-s10"])
V("doom-claims-gram", BY, "Doom claims Gram and a prophecy of Doomsday",
  "Doctor Doom came to the Chronicler for Gram, the Sword of Truth. Before giving it up, the Chronicler recited its last prophecy of a War of Secrets and a World of Battle in which Doom would succeed.",
  "Butcher's Blasphemy", 2025.98, S10, 4, [("victor-von-doom", "instigator"), ("the-chronicler", "witness")], ["wiki-s10"])
V("chronal-friction-rift", P, "Moon Girl warns of the chronal friction-rift",
  "Moon Girl gathered the Champions and explained that a rift left by Punch Chronovium during the Alchemax incursion is wearing away the boundary between the Present and 2099 timelines. Unless they are separated, only one reality can survive.",
  "Butcher's Blasphemy", 2025.99, S10, 4, [("moon-girl", "leader"), ("punch-chronovium", "witness")], ["wiki-s10"])

# ---------------------------------------------------------------- relationships
rels = []


def R(s, t, kind, desc, srcs, tl=None, since=None, until=None):
    rels.append(dict(source=s, target=t, kind=kind, timeline=tl, description=desc,
                     since_event=since, until_event=until, sources=srcs))


R("doom-2099", "victor-von-doom", "variant", "Doom 2099 is the future variant of Victor von Doom, and the two compete to reshape reality.", ["wiki-doom2099", "wiki-galacta"])
R("doom-2099", "victor-von-doom", "rival", "The present and future Dooms each fight to bend the Chronoverses to their own will.", ["wiki-galacta", "wiki-doom"], since="timestream-entanglement")
R("x-tron", "ultron", "variant", "X-Tron is a new body that Ultron grew from Krakoa's Resurrection Protocols, and it carries his programming.", ["wiki-s2"], tl=T99, since="x-tron-born")
R("captain-america-present", "captain-america", "variant", "The dead Captain America of the Present Timeline and the Steve Rogers of 2099 are versions of the same man.", ["wiki-mrf-lore", "wiki-present"])
R("doctor-strange-collapsed", "doctor-strange", "variant", "The Collapsed Timeline's late Doctor Strange is a variant of the present Sorcerer Supreme.", ["wiki-collapsed"])
R("scarlet-witch-zombies", "scarlet-witch", "variant", "The Queen of the Dead is a zombified Scarlet Witch from the Marvel Zombies Timeline.", ["wiki-zombies"])
R("the-chronicler", "loki", "variant", "The Chronicler is an aged Loki who took up the role of recording history after his death.", ["wiki-s10"], since="loki-becomes-chronicler")
R("blood-chronovium", "chronovium", "variant", "Blood Chronovium is Chronovium changed by Dracula's blood.", ["wiki-chronovium"])
R("punch-chronovium", "chronovium", "variant", "Punch Chronovium is Chronovium overcharged by Cyclops' optic blasts.", ["wiki-chronovium"])
R("cynthia-von-doom", "victor-von-doom", "parent", "Cynthia von Doom is Victor von Doom's late mother.", ["wiki-doom"])
R("cynthia-von-doom", "doom-2099", "parent", "Cynthia von Doom is also the mother of Doom 2099, who lost his memories of her.", ["wiki-doom2099", "wiki-s5"])
R("galactus", "galacta", "parent", "Galactus is Galacta's father and urges her to accept her destiny as a devourer.", ["wiki-galacta"])
R("thor", "loki", "sibling", "Thor and Loki are brothers, divided by Loki's grab for Yggsgard.", ["wiki-s0", "wiki-s10"])
R("loki", "thor", "enemy", "Loki banished Thor to another timeline to take the throne of Yggsgard.", ["wiki-s0"], since="loki-seizes-yggsgard")
R("loki", "hela", "ally", "Loki and Hela agreed to help each other: Yggsgard for him, the power of Chronovium for her.", ["wiki-s0"], since="loki-seizes-yggsgard", until="hela-queen-in-black")
R("angela", "laussa", "sibling", "Angela is searching for her infant sister Laussa.", ["wiki-s4"])
R("angela", "hela", "enemy", "Angela pursues Hela, whose Valkyries took Laussa.", ["wiki-s4"])
R("hela", "knull", "ally", "Hela became Knull's Queen in Black in exchange for great power.", ["wiki-s3"], tl=MO, since="hela-queen-in-black", until="knull-defeated")
R("knull", "all-black", "creator", "Knull is the creator and first wielder of the Necrosword All-Black.", ["wiki-s3", "wiki-s10"])
R("gorr", "all-black", "ally", "All-Black chose Gorr, and he treats the sword as the only family he has left.", ["wiki-s10"], since="gorr-becomes-god-butcher")
R("gorr", "thor", "enemy", "Gorr fought Thor in Yggsgard, New York and the God Quarry.", ["wiki-s10"], since="gorr-attacks-yggsgard")
R("gorr", "loki", "enemy", "Gorr killed Loki with All-Black when he attacked Yggsgard.", ["wiki-s10"], since="gorr-attacks-yggsgard")
R("gorr", "khonshu", "enemy", "Gorr hunted Khonshu, dragged him from Thebes and held him at the God Quarry.", ["wiki-s9", "wiki-s10"], since="khonshu-exposed")
R("gorr", "apocalypse", "enemy", "Gorr killed Apocalypse with All-Black before his ascension.", ["wiki-s9"], tl=CO, since="apocalypse-murdered")
R("moon-knight", "khonshu", "member", "Moon Knight is the Fist and avatar of the moon god Khonshu.", ["wiki-s0", "wiki-s9"])
R("moon-knight", "khonshu", "rival", "Moon Knight turned against Khonshu after he found out about the god's massacres.", ["wiki-s9"], since="khonshu-exposed")
R("moon-knight", "gorr", "enemy", "Moon Knight fought Gorr at the God Quarry with the Eternity Mask's power.", ["wiki-s10"], since="battle-of-god-quarry")
R("victor-von-doom", "dracula", "other", "Doom gave Dracula Chronovium to start the Eternal Night, then betrayed him to take his essence.", ["wiki-s1", "wiki-doom"], since="eternal-night-falls", until="dracula-defeated")
R("victor-von-doom", "doctor-strange", "rival", "Strange refused Doom the Darkhold, and they dueled in the Sanctum Sanctorum.", ["wiki-s0"], since="doom-demands-darkhold")
R("victor-von-doom", "loki", "ally", "Doom and Loki traded Shou-Lao's chi for a Phoenix Feather.", ["wiki-s4"], since="loki-steals-chi")
R("victor-von-doom", "black-cat", "other", "Doom freed the Thieves Guild in exchange for the Tablet of Life and Time.", ["wiki-s7"], since="doom-gets-tablet")
R("victor-von-doom", "moon-knight", "ally", "To repay Khonshu's warning, Doom gave Moon Knight the Eternity Mask.", ["wiki-s10"], since="battle-of-god-quarry")
R("victor-von-doom", "mister-fantastic", "rival", "Reed Richards warned Doom to stop scheming and help to repair reality.", ["wiki-s3"])
R("doom-2099", "emma-frost", "other", "Doom 2099 made a secret pact with Emma Frost to drain Krakoa's chronal energy and defeat X-Tron.", ["wiki-s2"], tl=T99, since="doom-2099-erases-x-tron")
R("doom-2099", "ultron", "enemy", "Doom 2099 tried to erase Ultron from history, which drew Ultron back to Earth.", ["wiki-s2", "wiki-2099"], tl=T99)
R("doom-2099", "tyler-stone", "ally", "Doom 2099 traded Chronovium and help against the mutants for Alchemax's Punch Chronovium.", ["wiki-s8"], tl=T99, since="doom-2099-alchemax-deal")
R("doom-2099", "rogue", "enemy", "Doom 2099 broke into Rogue's room and took the contract from her.", ["wiki-s6"], since="doom-2099-takes-contract")
R("doom-2099", "the-hood", "enemy", "Doom 2099 snatched the Tablet of Death and Entropy from The Hood.", ["wiki-s9"], since="doom-2099-steals-tablet-of-death")
R("doom-2099", "peni-parker", "enemy", "Peni Parker fights off Doom 2099's Doombots to guard the Web's keepers.", ["wiki-s0"], tl=T99)
R("ultron", "iron-man", "other", "Tony Stark rebooted Ultron under a firewall that forces him to work with the heroes.", ["wiki-s2"], since="x-tron-born")
R("ultron", "x-tron", "rival", "The rebooted Ultron disagreed with X-Tron's plans and helped the heroes against it.", ["wiki-s2"], tl=T99)
R("ultron", "magneto", "enemy", "Ultron killed Magneto at the Gala and infected him with the Ultron Virus.", ["wiki-s2"], tl=T99, since="hellfire-gala-attack")
R("mister-fantastic", "shuri", "ally", "Reed and Shuri work across realities to undo the Entanglement.", ["wiki-mrf-lore"])
R("mister-fantastic", "iron-man", "ally", "Reed and Tony co-designed the TRD but argue over how to power it.", ["wiki-s1", "wiki-trd"])
R("mister-fantastic", "timestream-reintegration-device", "creator", "Reed Richards is a lead designer of the TRD.", ["wiki-trd", "wiki-mrf-lore"])
R("iron-man", "timestream-reintegration-device", "creator", "Tony Stark helped build the TRD and nicknamed it Trudy.", ["wiki-trd"])
R("shuri", "timestream-reintegration-device", "creator", "Shuri is one of the geniuses behind the TRD.", ["wiki-trd"])
R("mister-fantastic", "fantastic-four", "leader", "Reed Richards leads the Fantastic Four.", ["wiki-s1"])
R("invisible-woman", "fantastic-four", "member", "Sue Storm is a member of the Fantastic Four.", ["wiki-s1"])
R("human-torch", "fantastic-four", "member", "Johnny Storm is a member of the Fantastic Four.", ["wiki-s1"])
R("the-thing", "fantastic-four", "member", "Ben Grimm is a member of the Fantastic Four.", ["wiki-s1"])
R("mister-fantastic", "invisible-woman", "romance", "Reed and Sue are partners in the Fantastic Four.", ["wiki-s1"])
R("black-panther", "shuri", "sibling", "T'Challa and Shuri are the royal siblings of the Intergalactic Empire of Wakanda.", ["wiki-mosaic", "wiki-mrf-lore"])
R("black-panther", "intergalactic-empire-of-wakanda", "leader", "T'Challa rules the Intergalactic Empire of Wakanda.", ["wiki-bp-lore"])
R("black-panther", "bast", "member", "Bast chose T'Challa as her avatar, the Black Panther.", ["wiki-bp-lore"])
R("knull", "bast", "enemy", "Knull corrupted Bast until the Phoenix purged her.", ["wiki-s3"], until="phoenix-purifies-bast")
R("dracula", "black-panther", "enemy", "Dracula turned T'Challa into a vampire with Blood Chronovium.", ["wiki-s1"], since="black-panther-turned")
R("dracula", "blade", "enemy", "Dracula held and drained Blade, and Blade later turned him to stone.", ["wiki-s1", "wiki-blood-hunt"])
R("dracula", "ratatoskr", "enemy", "Dracula captured Ratatoskr and later made her a vampire.", ["wiki-s1", "wiki-blood-hunt"])
R("blade", "hela", "enemy", "Blade defeated Hela on Klyntar by drinking her blood.", ["wiki-s3"], tl=MO)
R("phoenix", "cyclops", "romance", "Jean Grey and Scott Summers are married, though the Entanglement cut their psychic link.", ["wiki-s8", "wiki-s7"])
R("phoenix", "scarlet-witch", "ally", "Jean and Wanda joined their powers against Knull.", ["wiki-s3"], tl=MO)
R("gambit", "rogue", "romance", "Gambit and Rogue are husband and wife; their wedding on Krakoa was interrupted and later completed.", ["wiki-s5", "wiki-s6"])
R("grandmaster", "gambit", "other", "The Grandmaster hired Gambit to steal the von Doom contract.", ["wiki-s5"], since="grandmaster-hires-gambit")
R("grandmaster", "the-collector", "rival", "The Grandmaster and the Collector play for control of their merged realm.", ["wiki-s5"])
R("the-collector", "elders-of-the-universe", "member", "The Collector is an Elder of the Universe.", ["wiki-s5"])
R("grandmaster", "elders-of-the-universe", "member", "The Grandmaster is an Elder of the Universe.", ["wiki-s5"])
R("the-collector", "deadpool", "other", "The Collector employed Deadpool to take beings from dying universes, until Deadpool turned on him.", ["wiki-s6"], until="museum-breakout")
R("the-collector", "elsa-bloodstone", "other", "The Collector hired Elsa Bloodstone to catch monsters for his zoo.", ["wiki-s6"], until="museum-breakout")
R("deadpool", "jeff-the-land-shark", "friend", "Deadpool took Jeff for the Collector but kept him as a travel companion for a time.", ["wiki-s6"])
R("deadpool", "psylocke", "enemy", "Deadpool kidnapped Psylocke from her dying timeline for the Collector.", ["wiki-s6", "wiki-watercolor"])
R("deadpool", "elsa-bloodstone", "ally", "Deadpool and Elsa freed the Museum's creatures and found them a home.", ["wiki-s6"], since="museum-breakout")
R("devil-dinosaur", "moon-girl", "friend", "Devil Dinosaur and Moon Girl share a deep bond and were split up by the Entanglement.", ["wiki-s8", "wiki-moongirl"])
R("the-punisher", "devil-dinosaur", "ally", "The Punisher rode Devil Dinosaur in the charge on Alchemax HQ.", ["wiki-s8"], since="alchemax-returned")
R("moon-girl", "alchemax", "enemy", "Alchemax held Moon Girl and forced her to study Punch Chronovium.", ["wiki-s8"], since="alchemax-captures-moon-girl", until="alchemax-returned")
R("cyclops", "alchemax", "enemy", "Alchemax imprisoned Cyclops and used his optic blasts as a power source.", ["wiki-s8"], since="alchemax-captures-moon-girl", until="white-phoenix")
R("tyler-stone", "alchemax", "leader", "Tyler Stone is a top executive of Alchemax.", ["wiki-2099", "wiki-s8"])
R("emma-frost", "alchemax", "rival", "Emma Frost's Hellfire Protocol drove Alchemax out of its main markets.", ["wiki-s8"], tl=T99)
R("black-widow", "resistance-2099", "leader", "Black Widow leads the Resistance in 2099.", ["wiki-s0"])
R("the-punisher", "resistance-2099", "member", "Black Widow recruited the Punisher into the Resistance.", ["wiki-s0"])
R("wolverine", "resistance-2099", "ally", "Wolverine had already formed ties with the Resistance.", ["wiki-s0"])
R("black-widow", "captain-america", "ally", "Black Widow freed Captain America from Alchemax and fought beside him.", ["wiki-s0"], tl=T99, since="widow-frees-captain-america")
R("captain-america", "winter-soldier", "friend", "Steve Rogers and Bucky Barnes are old wartime partners.", ["wiki-cap-lore", "wiki-s0"])
R("hawkeye", "winter-soldier", "friend", "Hawkeye risked a solo rescue to free his friend Bucky from Hydra.", ["wiki-s0"])
R("winter-soldier", "hydra", "enemy", "Hydra's Occult Ops captured and experimented on the Winter Soldier.", ["wiki-s0"])
R("winter-soldier", "wolverine", "enemy", "Bucky confessed that he had killed Logan's family under Hydra control, and Logan later forgave him.", ["wiki-s9"])
R("spider-zero", "master-weaver", "mentor", "The Master Weaver trained Spider-Zero until he banished her.", ["wiki-s0", "wiki-galacta"], until="spider-zero-banished")
R("spider-zero", "web-warriors", "leader", "Spider-Zero assembled the Web-Warriors.", ["wiki-s0"], since="spider-zero-banished")
R("spider-man", "web-warriors", "member", "Peter Parker joined Spider-Zero's Web-Warriors.", ["wiki-s0"])
R("peni-parker", "web-warriors", "member", "Peni Parker was the first to stand with Spider-Zero as the Web-Warriors gathered.", ["wiki-2099"])
R("spider-man", "black-cat", "ally", "Spider-Man and Black Cat planned the Vault breakout together.", ["wiki-s7"], since="vault-breakout")
R("spider-man", "captain-america-present", "friend", "The Present Timeline's Captain America died saving Spider-Man.", ["wiki-s7", "wiki-s10"])
R("star-lord", "guardians-of-the-galaxy", "leader", "Star-Lord leads the Guardians of the Galaxy.", ["wiki-starlord-lore"])
R("rocket-raccoon", "guardians-of-the-galaxy", "member", "Rocket is a member of the Guardians.", ["wiki-s3"])
R("groot", "guardians-of-the-galaxy", "member", "Groot is a member of the Guardians.", ["wiki-s3"])
R("mantis", "guardians-of-the-galaxy", "member", "Mantis is a member of the Guardians.", ["wiki-mosaic"])
R("rocket-raccoon", "groot", "friend", "Rocket and Groot have been partners since Star-Lord recruited them on Hala.", ["wiki-s3"])
R("mantis", "loki", "friend", "Mantis grew fond of Loki and was heartbroken by his death.", ["wiki-s10"])
R("venom", "knull", "enemy", "Venom fought Knull on Klyntar with the Sword of Dracula.", ["wiki-s3", "wiki-venom-lore"], tl=MO)
R("magik", "venom", "other", "Magik once held Venom captive in her timeline's war.", ["wiki-venom-lore"], tl=CO)
R("magneto", "scarlet-witch", "family", "Magneto treats the Collapsed Timeline's Wanda as his daughter from another timeline.", ["wiki-s0"])
R("magneto", "x-men", "leader", "Magneto leads mutantkind on Krakoa.", ["wiki-s0"])
R("storm", "x-men", "member", "Storm is a Krakoan X-Men member.", ["wiki-s0"])
R("emma-frost", "quiet-council", "member", "Emma Frost sits on Krakoa's Quiet Council.", ["wiki-s2"])
R("wolverine", "x-men", "member", "Wolverine is a Krakoan mutant hero.", ["wiki-s2"])
R("cyclops", "x-men", "member", "Cyclops is one of the X-Men.", ["wiki-s8"])
R("psylocke", "x-men", "member", "Psylocke found a trusted family among the X-Men.", ["wiki-s9"])
R("jubilee", "shogo-lee", "parent", "Jubilee is the mother of Shogo Lee.", ["wiki-present", "wiki-s9"])
R("jubilee", "apocalypse", "ally", "Jubilee served Apocalypse as his Horseman of Famine.", ["wiki-s9"], tl=CO, since="jubilee-joins-apocalypse", until="apocalypse-murdered")
R("jubilee", "horsemen-of-death", "member", "Jubilee is one of the four Horsemen.", ["wiki-s8", "wiki-s9"])
R("apocalypse", "clan-akkaba", "leader", "Apocalypse leads Clan Akkaba.", ["wiki-collapsed"])
R("apocalypse", "horsemen-of-death", "leader", "Apocalypse commands his four Horsemen.", ["wiki-s8"])
R("apocalypse", "faith-harvesting-engine", "creator", "Apocalypse built the Faith-Harvesting Engine.", ["wiki-s9"])
R("loki", "psylocke", "enemy", "Loki killed Psylocke in Thebes for her blood and framed Magik.", ["wiki-s9"], since="thebes-investigation")
R("the-hood", "gambit", "enemy", "The Hood shot Gambit in Thebes to reach the Tablet first.", ["wiki-s9"], since="thebes-investigation")
R("black-cat", "gambit", "ally", "Gambit made a deal with Black Cat to fetch the Tablet of Death and Entropy.", ["wiki-s9"])
R("black-cat", "thieves-guild", "leader", "Black Cat became Guildmaster of New York's Thieves Guild.", ["wiki-s7", "wiki-s9"], since="doom-gets-tablet")
R("kingpin", "black-cat", "other", "Fisk hired Black Cat to steal the Tablet of Life and Time.", ["wiki-s7"])
R("kingpin", "captain-america", "enemy", "Fisk jailed Captain America in the Vault without a trial.", ["wiki-s7"], since="super-hero-ban", until="vault-breakout")
R("white-fox", "iron-fist", "friend", "Lin Lie once saved White Fox's life, and she gave him the last shard of the Sword of Fu Xi.", ["wiki-s7"])
R("white-fox", "tiger-division", "leader", "White Fox is the director of Tiger Division.", ["wiki-s7"])
R("luna-snow", "tiger-division", "member", "Luna Snow is a member of Tiger Division.", ["wiki-s7"])
R("namor", "luna-snow", "enemy", "Namor attacked Jeju Island during Luna Snow's concert.", ["wiki-present"])
R("namor", "magneto", "ally", "Magneto invited his old ally Namor to Krakoa to discuss an alliance.", ["wiki-present"])
R("iron-fist", "shou-lao", "member", "Lin Lie is Shou-Lao's chosen Immortal Weapon, the Iron Fist.", ["wiki-ironfist-lore", "wiki-s4"])
R("iron-fist", "daredevil", "rival", "Lin Lie beat Daredevil in the final of the Shenloong Tournament.", ["wiki-s4"], since="shenloong-tournament")
R("iron-fist", "laussa", "other", "Lin Lie cared for the infant Laussa after she was found in K'un-Lun.", ["wiki-s4"])
R("daredevil", "yinglong", "member", "Daredevil serves as the champion of the spirit Yinglong.", ["wiki-s4"])
R("daredevil", "eighth-city", "leader", "Daredevil leads the Eighth City.", ["wiki-s4"])
R("hulk", "thor", "ally", "Banner sent the banished Thor to rest at Bloodstone Manor.", ["wiki-collapsed"], tl=CO)
R("thor", "elsa-bloodstone", "ally", "Thor saved Elsa's brother and helped her map her ruined world.", ["wiki-s6", "wiki-collapsed"], tl=CO)
R("scarlet-witch", "doctor-strange", "ally", "Wanda helped Strange while he was lost in the Astral Plane, hoping for help in return.", ["wiki-s0"])
R("galacta", "chronovium", "other", "Galacta feeds on Chronovium crystals.", ["wiki-galacta", "wiki-chronovium"])
R("galacta", "jeff-the-land-shark", "friend", "Galacta adores Jeff and has claimed him as her own.", ["wiki-galacta"])
R("storm", "krakoa", "other", "Storm guided Krakoa through the timestorm into 2099.", ["wiki-s0"], since="krakoa-carried-to-2099")
R("loki", "yggsgard", "leader", "Loki rules Yggsgard as its king.", ["wiki-s0", "wiki-s10"], since="loki-seizes-yggsgard")
R("knull", "klyntar", "leader", "Knull is imprisoned in the core of Klyntar and rules its symbiotes.", ["wiki-s3", "official-home"], until="knull-defeated")
R("gorr", "klyntar", "leader", "Gorr took up the role of King in Black and went to Klyntar.", ["wiki-s10"], since="gorr-king-in-black")
R("spider-man", "mjolnir", "other", "The God Tempest judged Spider-Man worthy of Mjolnir's power.", ["wiki-s10"], since="battle-of-god-quarry")
R("storm", "spider-man", "ally", "Storm, Spider-Man and Moon Knight together fought Gorr at the God Quarry.", ["wiki-s10"], since="battle-of-god-quarry")
R("mantis", "the-chronicler", "friend", "Mantis convinced the Chronicler to change his account and bring Thor back.", ["wiki-s10"], since="thor-restored")
R("moon-girl", "mister-fantastic", "ally", "Moon Girl sent Reed the plans for the mini TRD and Devil's armor.", ["wiki-s8"])
R("psylocke", "mantis", "ally", "Psylocke, Mantis and Jeff escaped the Collector's Museum together.", ["wiki-te", "wiki-mosaic"])

out = dict(
    game=dict(slug="marvel-rivals", name="Marvel Rivals",
              calendar="There is no shared in-universe calendar: the Present and Collapsed timelines are set in the present day (mid-2020s) and the 2099 Timeline in 2099, so lore is labeled by the game season that told it, and sort_key places every event on one present-day axis (Timestream Entanglement = 2025.0, about 0.1 per season), with older backstory keyed to approximate years.",
              description="Marvel Rivals is a free-to-play team-based hero shooter by NetEase Games, released on 6 December 2024. Its story starts when Doctor Doom and Doom 2099 trigger the Timestream Entanglement, which breaks the multiverse into Chronoverses and throws heroes from different realities together. Each season adds a new story arc told through Gallery Cards, Hero Stories, events and map descriptions."),
    wiki=dict(base="https://marvelrivals.fandom.com/wiki/", api="https://marvelrivals.fandom.com/api.php", license="CC BY-SA 3.0",
              notes="Fandom is the active wiki (MediaWiki 1.43, about 3,200 articles, edits on the day of research). The marvelrivals.wiki.gg fork is inactive (64 articles, no recent edits). action=parse&page=<Page>&prop=wikitext&format=json with redirects=1 worked with a browser User-Agent and no rate limiting at about 3 requests per second. Most useful: Category:Lore, Category:Chronoverses, Category:Seasonal Storyline, the per-season 'Season N: <Title>/Lore' pages (condensed chronological story), '<Hero>/Lore' pages (full Hero Story text) and the 'Present/2099/Mosaic/Collapsed Timeline' pages, which list each character's Chronoverse of origin. Many chronoverse pages carry a LoreDeduction notice, so some origin assignments are fan inference."),
    sources=sources, timelines=timelines, entities=entities, events=events, relationships=rels)

# ---------------- validation
skeys = {s["key"] for s in sources}
tls = {t["slug"] for t in timelines}
ents = {e["slug"] for e in entities}
evs = {e["slug"] for e in events}
errs = []
for coll, name in [(entities, "entity"), (events, "event")]:
    seen = set()
    for x in coll:
        if x["slug"] in seen:
            errs.append(f"dup {name} {x['slug']}")
        seen.add(x["slug"])
for t in timelines:
    if t["parent"] and t["parent"] not in tls:
        errs.append("bad parent " + t["slug"])
for e in entities:
    if e["timeline"] and e["timeline"] not in tls: errs.append("ent tl " + e["slug"])
    if e["variant_of"] and e["variant_of"] not in ents: errs.append("ent var " + e["slug"])
    if not e["sources"] or any(s not in skeys for s in e["sources"]): errs.append("ent src " + e["slug"])
for v in events:
    if v["timeline"] not in tls: errs.append("ev tl " + v["slug"])
    for p in v["participants"]:
        if p["entity"] not in ents: errs.append(f"ev part {v['slug']} {p['entity']}")
    if not v["sources"] or any(s not in skeys for s in v["sources"]): errs.append("ev src " + v["slug"])
    if not 1 <= v["importance"] <= 5: errs.append("imp " + v["slug"])
KINDS = set("family sibling parent romance ally friend rival enemy mentor member leader creator variant other".split())
for r in rels:
    for k in ("source", "target"):
        if r[k] not in ents: errs.append(f"rel {k} {r[k]}")
    if r["kind"] not in KINDS: errs.append("rel kind " + r["kind"])
    if r["timeline"] and r["timeline"] not in tls: errs.append("rel tl")
    for k in ("since_event", "until_event"):
        if r[k] and r[k] not in evs: errs.append(f"rel {k} {r[k]}")
    if not r["sources"] or any(s not in skeys for s in r["sources"]): errs.append("rel src " + r["source"])
used = set()
for x in entities + events + rels:
    used.update(x["sources"])
unused = skeys - used
heroes = 54
print("errors:", errs)
print("unused sources:", unused)
print("counts: sources", len(sources), "timelines", len(timelines), "entities", len(entities), "events", len(events), "relationships", len(rels))
if not errs:
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("written", OUT)
