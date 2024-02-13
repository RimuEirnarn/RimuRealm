# Rimu Realm

This game uses curses to deal with layout in CLI.

> [!INFO]
> This may be a mouthful explanatory with complicated choice of words.

## System Mechanics

The game is a turn-based fantasy game so we must define the system to be used.

### Power Scaling

At heart of RPG game, there lies stats such as HP, Max HP, MP, Max MP, so on.
We will use these stats, including the basic stats such as STR, INT, CHA, ...

#### How are basic attributes are referenced and used

`STR` -> Strength, scaling `Physical DMG`
`VIT` -> Vitality, scaling character's `Max HP` and some `DEF`
`INT` -> Intelligence, a reduce scaling for character's `Max EXP` for leveling up. Maximum is 100.
`WLP` -> Willpower, scaling character's `Magical ATK` and `Magical RES`
`BRV` -> Bravery, scaling character's `Crit Rate` and `Crit DMG`
`END` -> Endurance, scaling character's `DEF`, `Max HP`, and `Debuff` resistence.
`SPD` -> Speed, scaling character's action.

#### How are attributes are calculated

`ATK` may uses `Level` and `STR` as basic scaling. This can be extended more by character's Weapon by increasing `Base ATK`.

`DEF` may uses `Level`, `END`, `VIT` as basic scaling. This can be extended by using `Equipment`

`Max HP` may uses `Level`, `VIT`, and `END` as basic scaling.

`Max MP` may uses `Rank Level` as scaling factor.

#### How are main attributes are calculated

`Level` has this linear equation:
`Max_EXP = Base_EXP + (Level - 1) * Linear_Scaling_Factor - (INT * INT_Scaling_Factor)%`

`Rank Level` has this exponential equation:
`Max_Rank_EXP = Base_Rank_EXP * Exponential_Factor^((Rank_Level - 0.1) * 10) - (INT * INT_Scaling_Factor)%`

If in case of `Level` < 1 or `Rank Level` < 1;
`Max_EXP = Base_EXP - (INT * INT_Scaling_Factor)%`

`Max_Rank_EXP = Base_EXP - (INT * INT_Scaling_Factor)%`

Maximum `Level` achieved is `10,000` and maximum `Rank Level` is `5.0`.

#### How ATK, etc. works

TODO

### Magika

This tells on how magic interacts

There are 9 magic types: `All`, `Light`, `Dark`, `Water`, `Fire`, `Ice`, `Earth`, `Wind`, `Electric`

#### Element Relationship

**NOTE**: `All` magic type has `+30%` basic `Magic RES` and `+30%` basic `Magic DMG`. This is relative to `Rank Level`
Each 0.1 of `Rank Level` give additional `1%` of `Magic RES` and `Magic DMG`. In total, the limit is `+80%`.

**NOTE**: `All` magic type is resistant to every magic type. `All` gives 0% `Magic RES` and `Magic DMG` to `All`.

| ELEMENT  | Light                | Dark               | Fire                | Water              | Ice                | Electric          | Earth              | Wind              |
|----------|----------------------|--------------------|---------------------|--------------------|--------------------|-------------------|--------------------|-------------------|
| Light    | 0% RES<br>0% DMG     | 15% RES<br>15% DMG | 0% RES<br>0% DMG    | 0% RES<br>0% DMG   | 0% RES<br>0% DMG   | 0% RES<br>0% DMG  | 0% RES<br>0% DMG   | 0% RES<br>0% DMG  |
| Dark     | -15% RES<br>-15% DMG | 0% RES<br>0% DMG   | 0% RES<br>0% DMG    | 0% RES<br>0% DMG   | 0% RES<br>0% DMG   | 0% RES<br>0% DMG  | 0% RES<br>0% DMG   | 0% RES<br>0% DMG  |
| Fire     | 0% RES<br>0% DMG     | 0% RES<br>0% DMG   | 0% RES<br>0% DMG    | -5% RES<br>0% DMG* | 5% RES<br>5% DMG** | 0% RES<br>0% DMG* | -20% RES<br>0% DMG | 0% RES<br>0% DMG* |
| Water    | 0% RES<br>0% DMG     | 0% RES<br>0% DMG   | 0% RES<br>15% DMG*  | 0% RES<br>0% DMG   | 0% RES<br>0% DMG*  | 0% RES<br>0% DMG* | 5% RES<br>0% DMG*  | 0% RES<br>0% DMG* |
| Ice      | 0% RES<br>0% DMG     | 0% RES<br>0% DMG   | -5% RES<br>5% DMG** | 0% RES<br>0% DMG*  | 0% RES<br>0% DMG   | 0% RES<br>0% DMG  | 0% RES<br>0% DMG   | 0% RES<br>0% DMG* |
| Electric | 0% RES<br>0% DMG     | 0% RES<br>0% DMG   | 0% RES<br>0% DMG*   | 0% RES<br>0% DMG*  | 0% RES<br>0% DMG   | 0% RES<br>0% DMG  | 0% RES<br>0% DMG   | 0% RES<br>0% DMG  |
| Earth    | 0% RES<br>0% DMG     | 0% RES<br>0% DMG   | 0% RES<br>0% DMG    | -5% RES<br>0% DMG* | 0% RES<br>0% DMG   | 20% RES<br>0% DMG | 0% RES<br>0% DMG   | 0% RES<br>0% DMG  |
| Wind     | 0% RES<br>0% DMG     | 0% RES<br>0% DMG   | 0% RES<br>0% DMG    | 0% RES<br>0% DMG   | 0% RES<br>0% DMG   | 0% RES<br>0% DMG  | 0% RES<br>0% DMG   | 0% RES<br>0% DMG  |

```
HOW TO READ ELEMENTS:
    Offending:
        Left to right (per-rows)

    Defending:
        Up to down (per-column)
```

Offending magic/element may be weaker than being the defending. Which is commonly the case.

\* May impose Reaction

\*\* May impose continuous reaction

\*\* `Fire` as offender may impose a `Melting` and reduces `Ice RES` and `Water RES` by -15%

\*\* `Ice` as offender may impose a `Melting` and increase to `Fire DMG` by 5%. Melting can sometimes turns fire off.

##### Reaction

Magic may impose `Reaction`, this apply certain things to happen like small explotion, etc.

| REACTIONS | Light | Dark | Fire     | Water         | Ice      | Electric      | Earth          | Wind    |
|-----------|-------|------|----------|---------------|----------|---------------|----------------|---------|
| Light     |       |      |          |               |          |               |                |         |
| Dark      |       |      |          |               |          |               |                |         |
| Fire      |       |      |          | Vaporise      | Melting  | Charged Fire  |                | Burning |
| Water     |       |      | Vanquish |               | Freezing | Charged Water | Mud            |         |
| Ice       |       |      |          | Frozen        |          |               |                |         |
| Electric  |       |      | Vanished | Charged Water |          |               | Charged Ground |         |
| Earth     |       |      |          | Soiled*       |          | Reduced       |                |         |
| Wind      |       |      |          |               |          |               | Heavy Wind**   | Tornado |

\* Soiled step 2, `Earth` as offender, it's `DMG` will be reduced due to inefficiency.
\*\* Heavy Wind occur if Rank Level of offender is more than defender by `0.2`

###### Vanquish

If water meets up with Fire, this creates a `Vanquish` and oftenly challenge to which will be reduced. If Rank Level of offender is higher by 0.1, `Fire` will be eliminated. If Rank Level is equal and is more than 2.0, a explosion happen which deals `AoE DMG`

###### Vaporise

If fire meets up with water, this creates a `Vaporise`. This reduces offender's DMG.

###### Melting

If fire meets up with ice, this creates a `Melting`. Which will eliminate ice and fire, chronologically.

###### Charged *

If eletric meets up with either fire, water, and earth, this may impose Vanished/Charged Fire/Charged Water/Charged Ground. If fire is the offender, this will deal `AoE DMG`. Charged Water and Charged Ground also deal `AoE DMG` while `Vanished` will eliminate eletric and fire.

###### Mud/Soiled

If water meets up with Earth, this will slow down defender/target by `30% Target SPD`.

If earth meets up with water, this will slow down defender/target by `10% Target SPD`.

###### Reduced

If Earth meets up with eletric, electric will be nullified.

###### Heavy Wind

If Wind meets up with Earth, deals `100% DMG + 20% Earth DMG`. This only occurs if offender's Rank Level is 0.2 higher than defender.

###### Burning

If fire and wind meets, this create `100% DMG + 20% Fire AoE DMG`, infused the fire with the wind and deals both DMG.

###### Tornado

If Wind meets up with Wind, this will deal `Big AoE DMG`. This can be infused with other elements such as `Fire` and `Water`.

