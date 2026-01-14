import Foundation

struct MilestoneTemplate {
    let id: String
    let title: String
    let description: String
    let category: MilestoneCategory
    let expectedAgeMonthsMin: Int
    let expectedAgeMonthsMax: Int
    let averageAgeMonths: Int
    let tips: String

    func toMilestone() -> Milestone {
        Milestone(
            id: id,
            title: title,
            description: description,
            category: category,
            expectedAgeMonthsMin: expectedAgeMonthsMin,
            expectedAgeMonthsMax: expectedAgeMonthsMax,
            averageAgeMonths: averageAgeMonths,
            tips: tips
        )
    }
}

struct MilestoneData {
    static let allMilestones: [MilestoneTemplate] = {
        var milestones: [MilestoneTemplate] = []

        // MARK: - 0-3 Months
        milestones.append(contentsOf: [
            MilestoneTemplate(
                id: "motor_0_3_lift_head",
                title: "Lifts head during tummy time",
                description: "Can lift head briefly while lying on tummy",
                category: .motor,
                expectedAgeMonthsMin: 1,
                expectedAgeMonthsMax: 3,
                averageAgeMonths: 2,
                tips: "Practice tummy time for a few minutes several times a day. Use colorful toys to encourage head lifting."
            ),
            MilestoneTemplate(
                id: "motor_0_3_hands_fists",
                title: "Opens and closes hands",
                description: "Moves from tight fists to open hands regularly",
                category: .motor,
                expectedAgeMonthsMin: 1,
                expectedAgeMonthsMax: 3,
                averageAgeMonths: 2,
                tips: "Let baby grasp your finger. This helps develop hand control."
            ),
            MilestoneTemplate(
                id: "social_0_3_smile",
                title: "First social smile",
                description: "Smiles in response to your smile or voice",
                category: .social,
                expectedAgeMonthsMin: 1,
                expectedAgeMonthsMax: 3,
                averageAgeMonths: 2,
                tips: "Smile and talk to your baby often. They learn to smile by watching you!"
            ),
            MilestoneTemplate(
                id: "language_0_3_coos",
                title: "Coos and makes sounds",
                description: "Makes cooing sounds like 'ooh' and 'aah'",
                category: .language,
                expectedAgeMonthsMin: 2,
                expectedAgeMonthsMax: 4,
                averageAgeMonths: 3,
                tips: "Talk back when baby coos. This back-and-forth builds language skills."
            ),
            MilestoneTemplate(
                id: "cognitive_0_3_follows_face",
                title: "Follows faces with eyes",
                description: "Watches and follows your face as you move",
                category: .cognitive,
                expectedAgeMonthsMin: 1,
                expectedAgeMonthsMax: 3,
                averageAgeMonths: 2,
                tips: "Move slowly side to side while your face is close. Baby will learn to track movement."
            ),
        ])

        // MARK: - 4-6 Months
        milestones.append(contentsOf: [
            MilestoneTemplate(
                id: "motor_4_6_roll_over",
                title: "Rolls over (tummy to back)",
                description: "Can roll from tummy to back independently",
                category: .motor,
                expectedAgeMonthsMin: 3,
                expectedAgeMonthsMax: 6,
                averageAgeMonths: 4,
                tips: "During tummy time, place toys slightly to the side to encourage rolling."
            ),
            MilestoneTemplate(
                id: "motor_4_6_roll_back_tummy",
                title: "Rolls over (back to tummy)",
                description: "Can roll from back to tummy independently",
                category: .motor,
                expectedAgeMonthsMin: 4,
                expectedAgeMonthsMax: 7,
                averageAgeMonths: 5,
                tips: "This usually comes after rolling tummy-to-back. Give lots of floor time to practice."
            ),
            MilestoneTemplate(
                id: "motor_4_6_sits_support",
                title: "Sits with support",
                description: "Can sit upright when supported by hands or pillows",
                category: .motor,
                expectedAgeMonthsMin: 4,
                expectedAgeMonthsMax: 6,
                averageAgeMonths: 5,
                tips: "Use a nursing pillow or sit behind baby for support while building core strength."
            ),
            MilestoneTemplate(
                id: "motor_4_6_reaches",
                title: "Reaches for toys",
                description: "Reaches out to grab objects of interest",
                category: .motor,
                expectedAgeMonthsMin: 3,
                expectedAgeMonthsMax: 5,
                averageAgeMonths: 4,
                tips: "Offer toys at arm's length. Bright, noisy toys encourage reaching."
            ),
            MilestoneTemplate(
                id: "language_4_6_babbles",
                title: "Babbles consonant sounds",
                description: "Makes babbling sounds with consonants like 'ba', 'da', 'ga'",
                category: .language,
                expectedAgeMonthsMin: 4,
                expectedAgeMonthsMax: 7,
                averageAgeMonths: 6,
                tips: "Repeat baby's sounds back to them. Narrate your day to expose them to more sounds."
            ),
            MilestoneTemplate(
                id: "social_4_6_laughs",
                title: "Laughs out loud",
                description: "Produces genuine belly laughs when amused",
                category: .social,
                expectedAgeMonthsMin: 3,
                expectedAgeMonthsMax: 5,
                averageAgeMonths: 4,
                tips: "Play peek-a-boo, make funny faces, and be silly together!"
            ),
            MilestoneTemplate(
                id: "cognitive_4_6_recognizes_faces",
                title: "Recognizes familiar faces",
                description: "Shows recognition of parents and caregivers",
                category: .cognitive,
                expectedAgeMonthsMin: 3,
                expectedAgeMonthsMax: 5,
                averageAgeMonths: 4,
                tips: "Baby may show excitement when seeing familiar people. This is a big cognitive step!"
            ),
            MilestoneTemplate(
                id: "motor_4_6_transfers_hands",
                title: "Transfers objects between hands",
                description: "Can pass a toy from one hand to the other",
                category: .motor,
                expectedAgeMonthsMin: 5,
                expectedAgeMonthsMax: 7,
                averageAgeMonths: 6,
                tips: "Offer toys and watch baby explore passing them hand to hand."
            ),
        ])

        // MARK: - 7-9 Months
        milestones.append(contentsOf: [
            MilestoneTemplate(
                id: "motor_7_9_sits_alone",
                title: "Sits without support",
                description: "Can sit independently without any support",
                category: .motor,
                expectedAgeMonthsMin: 6,
                expectedAgeMonthsMax: 9,
                averageAgeMonths: 7,
                tips: "Once sitting, place toys around baby to encourage reaching while balancing."
            ),
            MilestoneTemplate(
                id: "motor_7_9_crawls",
                title: "Crawls",
                description: "Moves across the floor on hands and knees",
                category: .motor,
                expectedAgeMonthsMin: 6,
                expectedAgeMonthsMax: 10,
                averageAgeMonths: 8,
                tips: "Some babies skip crawling entirely! Scooting, army crawling, or rolling are also normal."
            ),
            MilestoneTemplate(
                id: "motor_7_9_pulls_stand",
                title: "Pulls to standing",
                description: "Pulls up to stand using furniture for support",
                category: .motor,
                expectedAgeMonthsMin: 7,
                expectedAgeMonthsMax: 11,
                averageAgeMonths: 9,
                tips: "Make sure furniture is stable. Baby will use anything nearby to pull up!"
            ),
            MilestoneTemplate(
                id: "motor_7_9_pincer",
                title: "Pincer grasp developing",
                description: "Begins to pick up small objects with thumb and finger",
                category: .motor,
                expectedAgeMonthsMin: 7,
                expectedAgeMonthsMax: 10,
                averageAgeMonths: 9,
                tips: "Offer small, safe foods like puffs to practice. Watch for choking hazards."
            ),
            MilestoneTemplate(
                id: "language_7_9_responds_name",
                title: "Responds to name",
                description: "Looks or turns when their name is called",
                category: .language,
                expectedAgeMonthsMin: 5,
                expectedAgeMonthsMax: 9,
                averageAgeMonths: 7,
                tips: "Use baby's name often when talking to them. Make eye contact when saying it."
            ),
            MilestoneTemplate(
                id: "language_7_9_understands_no",
                title: "Understands 'no'",
                description: "Pauses or responds when told 'no'",
                category: .language,
                expectedAgeMonthsMin: 7,
                expectedAgeMonthsMax: 10,
                averageAgeMonths: 9,
                tips: "Baby understands your tone and the word. Be consistent but gentle."
            ),
            MilestoneTemplate(
                id: "social_7_9_stranger_anxiety",
                title: "Shows stranger anxiety",
                description: "Is wary of unfamiliar people",
                category: .social,
                expectedAgeMonthsMin: 6,
                expectedAgeMonthsMax: 10,
                averageAgeMonths: 8,
                tips: "This is actually a positive sign of healthy attachment! Give baby time to warm up."
            ),
            MilestoneTemplate(
                id: "cognitive_7_9_object_permanence",
                title: "Understands object permanence",
                description: "Looks for dropped or hidden toys",
                category: .cognitive,
                expectedAgeMonthsMin: 6,
                expectedAgeMonthsMax: 9,
                averageAgeMonths: 8,
                tips: "Play hide-and-seek with toys under blankets. Baby learns things exist even when hidden!"
            ),
            MilestoneTemplate(
                id: "social_7_9_waves",
                title: "Waves bye-bye",
                description: "Waves in response to bye-bye or independently",
                category: .social,
                expectedAgeMonthsMin: 8,
                expectedAgeMonthsMax: 12,
                averageAgeMonths: 10,
                tips: "Wave to baby often. They learn by imitation!"
            ),
        ])

        // MARK: - 10-12 Months
        milestones.append(contentsOf: [
            MilestoneTemplate(
                id: "motor_10_12_cruises",
                title: "Cruises along furniture",
                description: "Walks sideways while holding onto furniture",
                category: .motor,
                expectedAgeMonthsMin: 8,
                expectedAgeMonthsMax: 12,
                averageAgeMonths: 10,
                tips: "Arrange furniture close together so baby can move from piece to piece."
            ),
            MilestoneTemplate(
                id: "motor_10_12_stands_alone",
                title: "Stands alone briefly",
                description: "Can stand without support for a few seconds",
                category: .motor,
                expectedAgeMonthsMin: 9,
                expectedAgeMonthsMax: 13,
                averageAgeMonths: 11,
                tips: "Once cruising confidently, baby may let go briefly. Celebrate these moments!"
            ),
            MilestoneTemplate(
                id: "motor_10_12_first_steps",
                title: "Takes first steps",
                description: "Walks a few steps independently",
                category: .motor,
                expectedAgeMonthsMin: 9,
                expectedAgeMonthsMax: 15,
                averageAgeMonths: 12,
                tips: "Some babies walk at 9 months, others at 15+ months. Both are normal!"
            ),
            MilestoneTemplate(
                id: "language_10_12_first_word",
                title: "Says first word",
                description: "Uses one or more words with meaning (mama, dada, etc.)",
                category: .language,
                expectedAgeMonthsMin: 9,
                expectedAgeMonthsMax: 14,
                averageAgeMonths: 12,
                tips: "Label everything! 'This is a ball. Ball!' Repetition builds vocabulary."
            ),
            MilestoneTemplate(
                id: "language_10_12_gestures",
                title: "Uses gestures",
                description: "Points, waves, or uses other gestures to communicate",
                category: .language,
                expectedAgeMonthsMin: 9,
                expectedAgeMonthsMax: 12,
                averageAgeMonths: 11,
                tips: "Respond to baby's gestures. When they point, name what they're pointing at."
            ),
            MilestoneTemplate(
                id: "cognitive_10_12_imitates",
                title: "Imitates actions",
                description: "Copies simple actions like clapping or waving",
                category: .cognitive,
                expectedAgeMonthsMin: 9,
                expectedAgeMonthsMax: 12,
                averageAgeMonths: 10,
                tips: "Demonstrate actions slowly and repeat them. Baby learns through imitation."
            ),
            MilestoneTemplate(
                id: "social_10_12_plays_games",
                title: "Plays interactive games",
                description: "Enjoys and participates in peek-a-boo and patty-cake",
                category: .social,
                expectedAgeMonthsMin: 8,
                expectedAgeMonthsMax: 12,
                averageAgeMonths: 10,
                tips: "Simple games build social skills and turn-taking. Play often!"
            ),
            MilestoneTemplate(
                id: "motor_10_12_pincer_refined",
                title: "Refined pincer grasp",
                description: "Picks up small objects precisely with thumb and forefinger",
                category: .motor,
                expectedAgeMonthsMin: 9,
                expectedAgeMonthsMax: 12,
                averageAgeMonths: 10,
                tips: "Baby can now pick up very small items. Keep choking hazards away!"
            ),
        ])

        // MARK: - 13-18 Months
        milestones.append(contentsOf: [
            MilestoneTemplate(
                id: "motor_13_18_walks_well",
                title: "Walks well",
                description: "Walks steadily without falling often",
                category: .motor,
                expectedAgeMonthsMin: 12,
                expectedAgeMonthsMax: 18,
                averageAgeMonths: 14,
                tips: "Provide safe spaces to practice. Expect lots of falls - they're learning!"
            ),
            MilestoneTemplate(
                id: "motor_13_18_climbs",
                title: "Climbs on furniture",
                description: "Climbs onto chairs, couches, and low furniture",
                category: .motor,
                expectedAgeMonthsMin: 12,
                expectedAgeMonthsMax: 18,
                averageAgeMonths: 15,
                tips: "Anchor heavy furniture. Baby will climb everything! Supervise closely."
            ),
            MilestoneTemplate(
                id: "motor_13_18_stacks_blocks",
                title: "Stacks 2-3 blocks",
                description: "Can stack blocks or cups on top of each other",
                category: .motor,
                expectedAgeMonthsMin: 12,
                expectedAgeMonthsMax: 18,
                averageAgeMonths: 15,
                tips: "Stacking develops fine motor skills and hand-eye coordination."
            ),
            MilestoneTemplate(
                id: "motor_13_18_scribbles",
                title: "Scribbles with crayons",
                description: "Makes marks on paper with crayon or marker",
                category: .motor,
                expectedAgeMonthsMin: 12,
                expectedAgeMonthsMax: 18,
                averageAgeMonths: 15,
                tips: "Use large, chunky crayons. Tape paper down so it doesn't move."
            ),
            MilestoneTemplate(
                id: "language_13_18_3_words",
                title: "Says 3-5 words",
                description: "Uses at least 3-5 words regularly and meaningfully",
                category: .language,
                expectedAgeMonthsMin: 12,
                expectedAgeMonthsMax: 18,
                averageAgeMonths: 15,
                tips: "Words may not be clear to everyone, but if baby uses them consistently, they count!"
            ),
            MilestoneTemplate(
                id: "language_13_18_follows_simple",
                title: "Follows simple instructions",
                description: "Follows one-step commands like 'Give me the ball'",
                category: .language,
                expectedAgeMonthsMin: 12,
                expectedAgeMonthsMax: 18,
                averageAgeMonths: 14,
                tips: "Use gestures along with words. 'Give me the ball' with an outstretched hand."
            ),
            MilestoneTemplate(
                id: "language_13_18_points_want",
                title: "Points to show wants",
                description: "Points to objects they want or are interested in",
                category: .language,
                expectedAgeMonthsMin: 11,
                expectedAgeMonthsMax: 15,
                averageAgeMonths: 13,
                tips: "When baby points, name the object and talk about it. This builds vocabulary."
            ),
            MilestoneTemplate(
                id: "cognitive_13_18_body_parts",
                title: "Identifies body parts",
                description: "Points to nose, eyes, mouth when asked",
                category: .cognitive,
                expectedAgeMonthsMin: 14,
                expectedAgeMonthsMax: 20,
                averageAgeMonths: 17,
                tips: "Play 'Where's your nose?' games. Touch and name body parts during bath time."
            ),
            MilestoneTemplate(
                id: "social_13_18_helps_dress",
                title: "Helps with dressing",
                description: "Cooperates by holding out arms or legs when dressing",
                category: .social,
                expectedAgeMonthsMin: 12,
                expectedAgeMonthsMax: 18,
                averageAgeMonths: 15,
                tips: "Ask 'Where's your arm?' and guide it through. This builds independence."
            ),
            MilestoneTemplate(
                id: "social_13_18_uses_spoon",
                title: "Uses spoon (with spilling)",
                description: "Attempts to feed self with spoon, even if messy",
                category: .motor,
                expectedAgeMonthsMin: 12,
                expectedAgeMonthsMax: 18,
                averageAgeMonths: 15,
                tips: "Let baby practice even if messy! Use thick foods like oatmeal that stick to spoons."
            ),
            MilestoneTemplate(
                id: "social_13_18_plays_pretend_simple",
                title: "Simple pretend play",
                description: "Pretends to drink from cup or talk on phone",
                category: .cognitive,
                expectedAgeMonthsMin: 14,
                expectedAgeMonthsMax: 20,
                averageAgeMonths: 17,
                tips: "Model pretend play - 'feeding' a stuffed animal or pretending to sleep."
            ),
        ])

        // MARK: - 19-24 Months (Ruby's current age range + immediate future)
        milestones.append(contentsOf: [
            MilestoneTemplate(
                id: "motor_19_24_runs",
                title: "Runs",
                description: "Runs with improving coordination",
                category: .motor,
                expectedAgeMonthsMin: 18,
                expectedAgeMonthsMax: 24,
                averageAgeMonths: 20,
                tips: "Running is walking sped up! Provide safe, open spaces to run."
            ),
            MilestoneTemplate(
                id: "motor_19_24_kicks_ball",
                title: "Kicks ball forward",
                description: "Can kick a ball forward while standing",
                category: .motor,
                expectedAgeMonthsMin: 18,
                expectedAgeMonthsMax: 24,
                averageAgeMonths: 21,
                tips: "Use a large, soft ball. Show baby how to kick by demonstrating."
            ),
            MilestoneTemplate(
                id: "motor_19_24_walks_stairs",
                title: "Walks up stairs with help",
                description: "Climbs stairs holding hand or railing",
                category: .motor,
                expectedAgeMonthsMin: 18,
                expectedAgeMonthsMax: 26,
                averageAgeMonths: 22,
                tips: "Hold hands and count steps together. Two feet per step is normal at this age."
            ),
            MilestoneTemplate(
                id: "motor_19_24_stacks_4_blocks",
                title: "Stacks 4-6 blocks",
                description: "Can build a tower of 4-6 blocks",
                category: .motor,
                expectedAgeMonthsMin: 18,
                expectedAgeMonthsMax: 24,
                averageAgeMonths: 21,
                tips: "Building and knocking down is fun! Both activities build skills."
            ),
            MilestoneTemplate(
                id: "language_19_24_50_words",
                title: "Uses 50+ words",
                description: "Has a vocabulary of approximately 50 or more words",
                category: .language,
                expectedAgeMonthsMin: 18,
                expectedAgeMonthsMax: 24,
                averageAgeMonths: 21,
                tips: "Count all words, even unclear ones. 'Baba' for bottle counts!"
            ),
            MilestoneTemplate(
                id: "language_19_24_two_words",
                title: "Combines two words",
                description: "Puts two words together like 'more milk' or 'daddy go'",
                category: .language,
                expectedAgeMonthsMin: 18,
                expectedAgeMonthsMax: 26,
                averageAgeMonths: 22,
                tips: "Model two-word phrases. When baby says 'milk', respond 'want milk?'"
            ),
            MilestoneTemplate(
                id: "language_19_24_names_pictures",
                title: "Names pictures in books",
                description: "Points to and names familiar pictures",
                category: .language,
                expectedAgeMonthsMin: 18,
                expectedAgeMonthsMax: 24,
                averageAgeMonths: 21,
                tips: "Read together daily. Point and ask 'What's this?' to encourage naming."
            ),
            MilestoneTemplate(
                id: "cognitive_19_24_sorts_shapes",
                title: "Sorts shapes or colors",
                description: "Can match or sort by shape or color",
                category: .cognitive,
                expectedAgeMonthsMin: 20,
                expectedAgeMonthsMax: 28,
                averageAgeMonths: 24,
                tips: "Shape sorters and simple puzzles help develop this skill."
            ),
            MilestoneTemplate(
                id: "cognitive_19_24_follows_2step",
                title: "Follows 2-step instructions",
                description: "Can follow two-part instructions like 'Get the ball and bring it here'",
                category: .cognitive,
                expectedAgeMonthsMin: 20,
                expectedAgeMonthsMax: 28,
                averageAgeMonths: 24,
                tips: "Start simple and build up. Give time to process between steps."
            ),
            MilestoneTemplate(
                id: "social_19_24_parallel_play",
                title: "Parallel play",
                description: "Plays alongside other children",
                category: .social,
                expectedAgeMonthsMin: 18,
                expectedAgeMonthsMax: 24,
                averageAgeMonths: 21,
                tips: "Toddlers play near but not truly with other children yet. This is normal!"
            ),
            MilestoneTemplate(
                id: "social_19_24_shows_affection",
                title: "Shows affection openly",
                description: "Gives hugs and kisses without prompting",
                category: .social,
                expectedAgeMonthsMin: 15,
                expectedAgeMonthsMax: 24,
                averageAgeMonths: 20,
                tips: "Model affection by hugging and kissing your child often."
            ),
            MilestoneTemplate(
                id: "motor_19_24_throws_ball",
                title: "Throws ball overhand",
                description: "Can throw a ball forward with overhand motion",
                category: .motor,
                expectedAgeMonthsMin: 18,
                expectedAgeMonthsMax: 24,
                averageAgeMonths: 21,
                tips: "Practice outside with soft balls. Make it a game!"
            ),
        ])

        // MARK: - 25-30 Months
        milestones.append(contentsOf: [
            MilestoneTemplate(
                id: "motor_25_30_jumps",
                title: "Jumps with both feet",
                description: "Can jump up with both feet leaving the ground",
                category: .motor,
                expectedAgeMonthsMin: 24,
                expectedAgeMonthsMax: 30,
                averageAgeMonths: 27,
                tips: "Hold hands and jump together. Count 1-2-3 and jump!"
            ),
            MilestoneTemplate(
                id: "motor_25_30_stairs_alternating",
                title: "Walks up stairs alternating feet",
                description: "Uses alternate feet going up stairs with support",
                category: .motor,
                expectedAgeMonthsMin: 24,
                expectedAgeMonthsMax: 36,
                averageAgeMonths: 30,
                tips: "Practice on playground stairs. Hold hand for safety."
            ),
            MilestoneTemplate(
                id: "motor_25_30_copies_circle",
                title: "Copies a circle",
                description: "Can draw a rough circle after watching demonstration",
                category: .motor,
                expectedAgeMonthsMin: 27,
                expectedAgeMonthsMax: 36,
                averageAgeMonths: 30,
                tips: "Draw shapes together. It doesn't need to be perfect!"
            ),
            MilestoneTemplate(
                id: "language_25_30_sentences",
                title: "Uses 2-3 word sentences",
                description: "Regularly speaks in short sentences",
                category: .language,
                expectedAgeMonthsMin: 24,
                expectedAgeMonthsMax: 30,
                averageAgeMonths: 27,
                tips: "Expand on what your child says. 'Big truck!' becomes 'Yes, that's a big red truck!'"
            ),
            MilestoneTemplate(
                id: "language_25_30_names_familiar",
                title: "Names familiar people",
                description: "Says names of family members and friends",
                category: .language,
                expectedAgeMonthsMin: 24,
                expectedAgeMonthsMax: 30,
                averageAgeMonths: 26,
                tips: "Look at family photos together and practice naming people."
            ),
            MilestoneTemplate(
                id: "language_25_30_understood",
                title: "Speech 50% understandable",
                description: "Strangers can understand about half of what child says",
                category: .language,
                expectedAgeMonthsMin: 24,
                expectedAgeMonthsMax: 30,
                averageAgeMonths: 27,
                tips: "If you understand what your child means, repeat it clearly back to them."
            ),
            MilestoneTemplate(
                id: "cognitive_25_30_pretend_complex",
                title: "Complex pretend play",
                description: "Acts out scenarios with dolls or figures",
                category: .cognitive,
                expectedAgeMonthsMin: 24,
                expectedAgeMonthsMax: 30,
                averageAgeMonths: 27,
                tips: "Provide props like play food, dolls, and cars. Join in their pretend world!"
            ),
            MilestoneTemplate(
                id: "social_25_30_takes_turns",
                title: "Takes turns (with help)",
                description: "Can take turns in simple games with adult guidance",
                category: .social,
                expectedAgeMonthsMin: 24,
                expectedAgeMonthsMax: 36,
                averageAgeMonths: 30,
                tips: "Practice turn-taking with rolling a ball back and forth."
            ),
            MilestoneTemplate(
                id: "social_25_30_notices_emotions",
                title: "Notices others' emotions",
                description: "Shows concern when someone is upset",
                category: .social,
                expectedAgeMonthsMin: 24,
                expectedAgeMonthsMax: 30,
                averageAgeMonths: 27,
                tips: "Name emotions. 'The baby is crying. She feels sad.' This builds empathy."
            ),
        ])

        // MARK: - 31-36 Months (2.5-3 years)
        milestones.append(contentsOf: [
            MilestoneTemplate(
                id: "motor_31_36_pedals_trike",
                title: "Pedals tricycle",
                description: "Can ride and pedal a tricycle",
                category: .motor,
                expectedAgeMonthsMin: 30,
                expectedAgeMonthsMax: 36,
                averageAgeMonths: 33,
                tips: "Start with a balance bike or tricycle. Practice pushing with feet first."
            ),
            MilestoneTemplate(
                id: "motor_31_36_uses_scissors",
                title: "Uses child scissors",
                description: "Can snip paper with child-safe scissors",
                category: .motor,
                expectedAgeMonthsMin: 30,
                expectedAgeMonthsMax: 42,
                averageAgeMonths: 36,
                tips: "Use child-safe scissors. Start with snipping, then progress to cutting lines."
            ),
            MilestoneTemplate(
                id: "motor_31_36_draws_person",
                title: "Draws a person (head + 1 part)",
                description: "Draws a simple person with head and at least one other part",
                category: .motor,
                expectedAgeMonthsMin: 33,
                expectedAgeMonthsMax: 42,
                averageAgeMonths: 36,
                tips: "Don't correct their drawings. Ask 'Tell me about your picture!'"
            ),
            MilestoneTemplate(
                id: "language_31_36_conversations",
                title: "Has conversations",
                description: "Engages in back-and-forth conversations with 2-3 exchanges",
                category: .language,
                expectedAgeMonthsMin: 30,
                expectedAgeMonthsMax: 36,
                averageAgeMonths: 33,
                tips: "Ask open-ended questions. 'What did you do today?' instead of yes/no questions."
            ),
            MilestoneTemplate(
                id: "language_31_36_asks_questions",
                title: "Asks 'what' and 'where' questions",
                description: "Asks questions like 'What's that?' and 'Where's mommy?'",
                category: .language,
                expectedAgeMonthsMin: 30,
                expectedAgeMonthsMax: 36,
                averageAgeMonths: 32,
                tips: "Answer questions patiently. Curiosity is a sign of healthy development!"
            ),
            MilestoneTemplate(
                id: "language_31_36_understood_75",
                title: "Speech 75% understandable",
                description: "Strangers can understand most of what child says",
                category: .language,
                expectedAgeMonthsMin: 30,
                expectedAgeMonthsMax: 36,
                averageAgeMonths: 33,
                tips: "If pronunciation isn't clear, gently model the correct sound without correcting."
            ),
            MilestoneTemplate(
                id: "cognitive_31_36_counts_3",
                title: "Counts to 3",
                description: "Can count at least 3 objects",
                category: .cognitive,
                expectedAgeMonthsMin: 30,
                expectedAgeMonthsMax: 40,
                averageAgeMonths: 35,
                tips: "Count everything! Steps, snacks, toys. Make counting part of daily life."
            ),
            MilestoneTemplate(
                id: "cognitive_31_36_knows_age",
                title: "Knows age and gender",
                description: "Can tell you their age and whether they're a boy or girl",
                category: .cognitive,
                expectedAgeMonthsMin: 30,
                expectedAgeMonthsMax: 42,
                averageAgeMonths: 36,
                tips: "Practice before birthday. 'How old will you be?' Hold up fingers."
            ),
            MilestoneTemplate(
                id: "social_31_36_plays_with_others",
                title: "Interactive play with peers",
                description: "Plays cooperatively with other children, not just alongside",
                category: .social,
                expectedAgeMonthsMin: 30,
                expectedAgeMonthsMax: 40,
                averageAgeMonths: 35,
                tips: "Arrange playdates. Supervision helps guide positive interactions."
            ),
            MilestoneTemplate(
                id: "social_31_36_independent_activities",
                title: "Independent activities",
                description: "Plays independently for 5-10 minutes",
                category: .social,
                expectedAgeMonthsMin: 30,
                expectedAgeMonthsMax: 36,
                averageAgeMonths: 33,
                tips: "Set up engaging activities and stay nearby but let child play alone."
            ),
            MilestoneTemplate(
                id: "motor_31_36_dresses_help",
                title: "Dresses with help",
                description: "Can put on some clothing with assistance",
                category: .motor,
                expectedAgeMonthsMin: 30,
                expectedAgeMonthsMax: 40,
                averageAgeMonths: 35,
                tips: "Start with easy items like elastic pants. Celebrate each success!"
            ),
        ])

        // MARK: - 37-42 Months (3-3.5 years)
        milestones.append(contentsOf: [
            MilestoneTemplate(
                id: "motor_37_42_hops_one_foot",
                title: "Hops on one foot",
                description: "Can hop on one foot 1-2 times",
                category: .motor,
                expectedAgeMonthsMin: 36,
                expectedAgeMonthsMax: 48,
                averageAgeMonths: 40,
                tips: "Hold hands and practice. Make it a game - hop like a bunny!"
            ),
            MilestoneTemplate(
                id: "motor_37_42_catches_ball",
                title: "Catches bounced ball",
                description: "Can catch a large ball that's been bounced to them",
                category: .motor,
                expectedAgeMonthsMin: 36,
                expectedAgeMonthsMax: 48,
                averageAgeMonths: 42,
                tips: "Use a large, soft ball. Bounce gently and say 'Ready? Catch!'"
            ),
            MilestoneTemplate(
                id: "motor_37_42_copies_square",
                title: "Copies a square",
                description: "Can draw a recognizable square after demonstration",
                category: .motor,
                expectedAgeMonthsMin: 40,
                expectedAgeMonthsMax: 54,
                averageAgeMonths: 48,
                tips: "Draw together. Circles and squares are building blocks for letters!"
            ),
            MilestoneTemplate(
                id: "language_37_42_tells_stories",
                title: "Tells simple stories",
                description: "Narrates events or tells simple stories",
                category: .language,
                expectedAgeMonthsMin: 36,
                expectedAgeMonthsMax: 48,
                averageAgeMonths: 42,
                tips: "Ask about their day. 'What happened at the park?' Listen actively."
            ),
            MilestoneTemplate(
                id: "language_37_42_says_name",
                title: "Says full name",
                description: "Can state first and last name when asked",
                category: .language,
                expectedAgeMonthsMin: 33,
                expectedAgeMonthsMax: 42,
                averageAgeMonths: 36,
                tips: "Practice full name. Make it a song! This is also a safety skill."
            ),
            MilestoneTemplate(
                id: "language_37_42_uses_plurals",
                title: "Uses plurals correctly",
                description: "Says 'cats', 'dogs', 'toys' correctly most of the time",
                category: .language,
                expectedAgeMonthsMin: 36,
                expectedAgeMonthsMax: 48,
                averageAgeMonths: 40,
                tips: "Gently model correct plurals. Some irregular plurals take longer."
            ),
            MilestoneTemplate(
                id: "cognitive_37_42_names_colors",
                title: "Names 4+ colors",
                description: "Can correctly name at least 4 colors",
                category: .cognitive,
                expectedAgeMonthsMin: 36,
                expectedAgeMonthsMax: 48,
                averageAgeMonths: 40,
                tips: "Point out colors everywhere. 'Look at the red car! What color is that flower?'"
            ),
            MilestoneTemplate(
                id: "cognitive_37_42_understands_time",
                title: "Understands time concepts",
                description: "Understands 'yesterday', 'today', 'tomorrow'",
                category: .cognitive,
                expectedAgeMonthsMin: 36,
                expectedAgeMonthsMax: 48,
                averageAgeMonths: 42,
                tips: "Talk about plans. 'Today we go to the store. Tomorrow we visit grandma.'"
            ),
            MilestoneTemplate(
                id: "social_37_42_shares",
                title: "Shares with others",
                description: "Willingly shares toys with friends (at least sometimes)",
                category: .social,
                expectedAgeMonthsMin: 36,
                expectedAgeMonthsMax: 48,
                averageAgeMonths: 42,
                tips: "Praise sharing when you see it. 'That was so kind to share your toy!'"
            ),
            MilestoneTemplate(
                id: "social_37_42_follows_rules",
                title: "Follows simple game rules",
                description: "Can play games with simple rules like hide-and-seek",
                category: .social,
                expectedAgeMonthsMin: 36,
                expectedAgeMonthsMax: 48,
                averageAgeMonths: 40,
                tips: "Simple board games and card games teach rule-following."
            ),
        ])

        // MARK: - 43-48 Months (3.5-4 years)
        milestones.append(contentsOf: [
            MilestoneTemplate(
                id: "motor_43_48_stands_one_foot",
                title: "Stands on one foot (5+ seconds)",
                description: "Can balance on one foot for 5 or more seconds",
                category: .motor,
                expectedAgeMonthsMin: 42,
                expectedAgeMonthsMax: 54,
                averageAgeMonths: 48,
                tips: "Practice being a flamingo! Count how long they can balance."
            ),
            MilestoneTemplate(
                id: "motor_43_48_uses_fork_spoon",
                title: "Uses fork and spoon well",
                description: "Eats most foods with utensils successfully",
                category: .motor,
                expectedAgeMonthsMin: 36,
                expectedAgeMonthsMax: 48,
                averageAgeMonths: 42,
                tips: "Practice makes perfect. Child-size utensils are easier to handle."
            ),
            MilestoneTemplate(
                id: "motor_43_48_dresses_self",
                title: "Dresses independently",
                description: "Can dress and undress with minimal help",
                category: .motor,
                expectedAgeMonthsMin: 42,
                expectedAgeMonthsMax: 54,
                averageAgeMonths: 48,
                tips: "Allow extra time in the morning. Independence takes patience!"
            ),
            MilestoneTemplate(
                id: "motor_43_48_buttons",
                title: "Buttons large buttons",
                description: "Can fasten and unfasten large buttons",
                category: .motor,
                expectedAgeMonthsMin: 42,
                expectedAgeMonthsMax: 54,
                averageAgeMonths: 48,
                tips: "Practice on dress-up clothes or a button board before real clothes."
            ),
            MilestoneTemplate(
                id: "language_43_48_complex_sentences",
                title: "Uses complex sentences",
                description: "Speaks in sentences of 5+ words with complex structure",
                category: .language,
                expectedAgeMonthsMin: 42,
                expectedAgeMonthsMax: 54,
                averageAgeMonths: 48,
                tips: "Model complex sentences. Read books with richer language."
            ),
            MilestoneTemplate(
                id: "language_43_48_asks_why",
                title: "Asks 'why' frequently",
                description: "Constantly asks 'why' questions",
                category: .language,
                expectedAgeMonthsMin: 36,
                expectedAgeMonthsMax: 48,
                averageAgeMonths: 42,
                tips: "This is great! Answer patiently. Sometimes ask 'Why do you think?'"
            ),
            MilestoneTemplate(
                id: "language_43_48_understood_100",
                title: "Speech fully understandable",
                description: "Strangers can understand almost everything child says",
                category: .language,
                expectedAgeMonthsMin: 42,
                expectedAgeMonthsMax: 54,
                averageAgeMonths: 48,
                tips: "Some sounds like 'r' and 'th' may still be developing. That's normal!"
            ),
            MilestoneTemplate(
                id: "cognitive_43_48_counts_10",
                title: "Counts to 10",
                description: "Can count to 10 and count 10 objects",
                category: .cognitive,
                expectedAgeMonthsMin: 42,
                expectedAgeMonthsMax: 54,
                averageAgeMonths: 48,
                tips: "Count real objects. Touch each one while counting for 1-to-1 correspondence."
            ),
            MilestoneTemplate(
                id: "cognitive_43_48_knows_letters",
                title: "Recognizes some letters",
                description: "Identifies at least 5-10 letters of the alphabet",
                category: .cognitive,
                expectedAgeMonthsMin: 42,
                expectedAgeMonthsMax: 60,
                averageAgeMonths: 48,
                tips: "Start with letters in their name. Point out letters in the environment."
            ),
            MilestoneTemplate(
                id: "cognitive_43_48_understands_same_different",
                title: "Understands same/different",
                description: "Can identify what's the same and different between objects",
                category: .cognitive,
                expectedAgeMonthsMin: 42,
                expectedAgeMonthsMax: 54,
                averageAgeMonths: 46,
                tips: "Play matching games. 'These are the same. That one is different!'"
            ),
            MilestoneTemplate(
                id: "social_43_48_plays_cooperatively",
                title: "Cooperative play",
                description: "Plays cooperatively with others, takes turns, shares",
                category: .social,
                expectedAgeMonthsMin: 42,
                expectedAgeMonthsMax: 54,
                averageAgeMonths: 48,
                tips: "Structured activities help. 'First Sarah's turn, then your turn!'"
            ),
            MilestoneTemplate(
                id: "social_43_48_expresses_emotions",
                title: "Expresses emotions verbally",
                description: "Can say 'I'm angry' or 'I'm sad' instead of just acting out",
                category: .social,
                expectedAgeMonthsMin: 42,
                expectedAgeMonthsMax: 54,
                averageAgeMonths: 48,
                tips: "Help label emotions. 'You look frustrated. Are you frustrated?'"
            ),
            MilestoneTemplate(
                id: "social_43_48_imagination",
                title: "Rich imaginative play",
                description: "Engages in elaborate pretend scenarios with multiple steps",
                category: .social,
                expectedAgeMonthsMin: 42,
                expectedAgeMonthsMax: 54,
                averageAgeMonths: 46,
                tips: "Provide props and join their imaginative worlds when invited!"
            ),
        ])

        return milestones
    }()

    static func milestonesForAgeRange(minMonths: Int, maxMonths: Int) -> [MilestoneTemplate] {
        return allMilestones.filter { milestone in
            milestone.expectedAgeMonthsMin <= maxMonths && milestone.expectedAgeMonthsMax >= minMonths
        }.sorted { $0.averageAgeMonths < $1.averageAgeMonths }
    }

    static func pastMilestones(forChildAgeMonths ageMonths: Int) -> [MilestoneTemplate] {
        return allMilestones.filter { milestone in
            milestone.expectedAgeMonthsMax < ageMonths
        }.sorted { $0.averageAgeMonths < $1.averageAgeMonths }
    }

    static func currentMilestones(forChildAgeMonths ageMonths: Int) -> [MilestoneTemplate] {
        return allMilestones.filter { milestone in
            milestone.expectedAgeMonthsMin <= ageMonths && milestone.expectedAgeMonthsMax >= ageMonths
        }.sorted { $0.averageAgeMonths < $1.averageAgeMonths }
    }

    static func upcomingMilestones(forChildAgeMonths ageMonths: Int, withinMonths: Int = 24) -> [MilestoneTemplate] {
        let futureAge = ageMonths + withinMonths
        return allMilestones.filter { milestone in
            milestone.expectedAgeMonthsMin > ageMonths && milestone.expectedAgeMonthsMin <= futureAge
        }.sorted { $0.averageAgeMonths < $1.averageAgeMonths }
    }

    static func milestonesByCategory(_ category: MilestoneCategory) -> [MilestoneTemplate] {
        return allMilestones.filter { $0.category == category }
            .sorted { $0.averageAgeMonths < $1.averageAgeMonths }
    }
}
