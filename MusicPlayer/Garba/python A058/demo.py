import pyttsx3
import speech_recognition as sr
import datetime
import time
import random

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


global audio

def speak(audio, rate=200):
    print("Jarvis:", audio)
    engine.setProperty('rate', rate)  # Set speech rate
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning! I am Jarvis Sir, Your Mental Health Therapist. how may I help you ")
    elif 12 <= hour < 18:
        speak("Good Afternoon! I am Jarvis Sir, Your Mental Health Therapist. how may I help you ?")
    else:
        speak("Good Evening! I am Jarvis Sir, Your Mental Health Therapist. how may I help you ?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.7
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            if loop_counter == 0 or loop_counter == 1:
                speak("No speech detected. Please try again.")
                return None  # Return None instead of "None"
            else:
                return None
        except sr.RequestError:
            speak("Request Error!, I am a Mental Health Therapist ask related to it")
            return None
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"You: {query}")
        # Check if the query contains exit keywords
        if any(word in query.lower() for word in ['exit', 'goodbye', 'quit']):
            speak("Goodbye!")
            exit()  # Exit the program
    except sr.UnknownValueError:
        if loop_counter == 0 or loop_counter == 1 :
            speak("Sorry, I couldn't understand that. Please try again.")
            return None  # Return None instead of "None"
    return query



# Define your mental health dictionary with predefined sentences
mental_health_dict = {
    'hello_hi':[
        "Hello!, how are you ?",
        "hello!",
        "Hi "
    ], 
    'depressed_sad_melancholic_blue_downcast_unhappy': [
        "It's important to remember that you're not alone. I'm here to listen and support you.",
        "I'm sorry to hear that you're feeling down. Remember, things will get better with time.",
        "You're stronger than you think. Keep pushing forward.",
        "Even on the darkest days, there's a glimmer of light. Hold on to that hope.",
        "Take each day as it comes, and be gentle with yourself. Healing takes time."
    ],
    'anxious_nervous_worried_tense_distressed_agitated': [
        "Take a few deep breaths. Remember that it's okay to feel anxious sometimes.",
        "Try to focus on the present moment. What's one thing you can do right now to feel better?",
        "Visualize a peaceful place. Imagine yourself there, surrounded by calmness.",
        "Anxiety may feel overwhelming, but remember that you've overcome challenges before. You can do it again.",
        "Focus on what you can control, and let go of the rest. You're stronger than you realize."
    ],
    'stressed_overwhelmed_burdened_overworked_frazzled': [
        "It sounds like you're feeling overwhelmed. Let's try to focus on one thing at a time.",
        "Remember to take breaks and practice self-care. You deserve to prioritize your well-being.",
        "You've overcome challenges before, and you'll overcome this one too. Take it one step at a time.",
        "Give yourself permission to rest. You don't have to do it all at once.",
        "Break tasks into smaller, more manageable steps. Progress, no matter how small, is still progress."
    ],
    'lonely_isolated_solitary_alone': [
        "Feeling lonely is tough, but reaching out to friends or loved ones can help.",
        "Consider joining a club or group where you can meet new people with shared interests.",
        "Take this time to focus on self-discovery and self-love. You are enough, just as you are.",
        "Know that loneliness is temporary. Reach out, and let someone in.",
        "Find comfort in activities that bring you joy, even if you're alone. Your happiness matters."
    ],
    'overwhelmed_burdened_swamped_overloaded_snowed_under': [
        "It's okay to feel overwhelmed sometimes. Take a step back and break tasks into smaller, manageable steps.",
        "You're capable of handling whatever comes your way. Remember to ask for help if you need it.",
        "Give yourself permission to prioritize your mental health. You can't pour from an empty cup.",
        "Take a moment to breathe and regroup. You've got this.",
        "Focus on progress, not perfection. Each step forward is a victory in itself."
    ],
    'good_happy_positive_content_satisfied_joyful': [
        "That's great to hear! Celebrate your victories, big and small.",
        "Keep up the positive attitude! You're on the right track.",
        "Enjoy the moment and savor the feeling of happiness.",
        "Spread positivity wherever you go. Your smile is contagious.",
        "Find gratitude in the little things. There's beauty all around you."
    ],
    'bad_sad_negative_unhappy_displeased': [
        "I'm sorry you're feeling this way. Remember, it's okay not to be okay sometimes.",
        "This too shall pass. You're strong enough to overcome any challenges.",
        "Take some time for self-care. Doing something you enjoy can help improve your mood.",
        "Acknowledge your emotions without judgment. It's okay to feel what you're feeling.",
        "Know that it's okay to reach out for support when you're struggling. You're not alone in this."
    ],
    'unmotivated': [
        "I understand how difficult it can be to feel low. Remember, you're not alone in this.",
        "Reach out to someone you trust and talk about how you're feeling. Sharing your emotions can lighten the burden.",
        "Take it one step at a time. Small positive actions can gradually lift your spirits.",
        "Focus on what inspires you and brings you joy. Let your passions guide you forward.",
        "Give yourself grace during times of low motivation. Rest and recharge as needed."
    ],
    'hopeless_desperate_disheartened': [
        "Feeling hopeless is tough, but remember that tomorrow is a new day with new possibilities.",
        "Even in the darkest moments, there's a glimmer of hope. Hold on to that light.",
        "You've overcome challenges before, and you'll find hope again. Keep moving forward.",
        "Surround yourself with people who uplift and inspire you. You deserve positivity in your life.",
        "Focus on the present moment and the small joys it brings. Hope can be found in unexpected places."
    ],
    'worthless_inferior_valueless_low_inadequate': [
        "You are worthy of love and respect, no matter what negative thoughts may say.",
        "Your worth isn't defined by external measures. You have inherent value as a human being.",
        "Challenge negative self-talk by reminding yourself of your strengths and accomplishments.",
        "Practice self-compassion and treat yourself with kindness. You deserve it.",
        "Surround yourself with people who recognize and appreciate your worth. You deserve to be valued."
    ],
    'guilty_ashamed_remorseful_contrite_culpable': [
        "Guilt is a natural emotion, but remember to forgive yourself. You're only human.",
        "Reflect on what you've learned from the situation and use it as an opportunity for growth.",
        "Practice self-compassion. Treat yourself with the same kindness you would offer a friend.",
        "Apologize and make amends if necessary, but also remember to forgive yourself.",
        "Focus on the lessons learned from your mistakes rather than dwelling on guilt and shame."
    ],
    'hopeful_optimistic_positive_confident_expectant': [
        "Hold on to that feeling of hope. It's a powerful force that can guide you through difficult times.",
        "Focus on the possibilities that lie ahead. You have the strength to create a brighter future.",
        "Even small steps toward your goals can reinforce your sense of hope and optimism.",
        "Surround yourself with positivity and people who believe in you. You're capable of amazing things.",
        "Trust in your abilities and the journey ahead. You have the power to shape your own destiny."
    ],
    'trapped_confined_captive_stranded_enclosed': [
        "Feeling trapped can be suffocating, but remember that there are always options, even if they're not immediately apparent.",
        "Explore ways to regain a sense of control over your life. Small changes can lead to greater freedom.",
        "Reach out for support from trusted friends, family, or professionals. You don't have to face this alone.",
        "Focus on the things you can control and let go of what you can't. Your freedom lies in your mindset.",
        "Find solace in the fact that change is inevitable. Even the most difficult situations are temporary."
    ],
    'lost_confused_disoriented_directionless_uncertain': [
        "Feeling lost is disorienting, but remember that it's okay not to have all the answers right now.",
        "Take time to explore your interests and passions. Sometimes, the path becomes clearer as you move forward.",
        "Trust that you'll find your way. Each step you take, no matter how small, brings you closer to where you're meant to be.",
        "Focus on the journey rather than the destination. Life's twists and turns often lead to unexpected opportunities.",
        "Embrace the uncertainty as an opportunity for growth and exploration. Your path will reveal itself in time."
    ],
    'paranoid_suspicious_distrustful_apprehensive': [
        "Feeling paranoid can be distressing, but try to remind yourself that your thoughts may not accurately reflect reality.",
        "Focus on grounding techniques, such as deep breathing or mindfulness, to help reduce feelings of paranoia.",
        "Consider seeking support from a therapist or counselor who can help you explore and address your concerns.",
        "Challenge irrational thoughts by questioning the evidence supporting them. Reality is often less frightening than our imaginations.",
        "Surround yourself with people you trust and who can offer a different perspective on your fears. You don't have to face them alone."
    ],
    'ashamed_embarrassed_humiliated_sorry': [
        "Feeling ashamed is difficult, but remember that everyone makes mistakes. It's a part of being human.",
        "Practice self-compassion and forgiveness. Treat yourself with the same kindness you would offer a friend.",
        "Focus on what you've learned from the situation and how you can grow from it, rather than dwelling on feelings of shame.",
        "Apologize and make amends if necessary, but also remember to forgive yourself. You're worthy of compassion and understanding.",
        "Surround yourself with people who accept you for who you are, flaws and all. You deserve love and acceptance."
    ],
    'restless_agitated_jittery_fidgety_unsettled': [
        "Feeling restless can be uncomfortable, but try to channel that energy into something productive or calming.",
        "Engage in activities that promote relaxation, such as meditation, yoga, or going for a walk in nature.",
        "Explore the underlying reasons behind your restlessness. Is there something you need to address or change in your life?",
        "Focus on the present moment rather than dwelling on future uncertainties. You have the power to find peace within yourself.",
        "Practice gratitude for the small moments of calmness and stillness in your day. Embrace the tranquility when it comes."
    ],
    'numb_unfeeling_insensitive': [
        "Feeling numb can be a coping mechanism, but it's important to address underlying emotions and seek support when needed.",
        "Try to reconnect with your emotions through creative expression, journaling, or talking to a trusted friend or therapist.",
        "Remember that it's okay to feel, even if those feelings are uncomfortable. Emotions are a natural part of the human experience.",
        "Practice self-compassion and kindness toward yourself. Allow yourself to experience your emotions fully, without judgment.",
        "Surround yourself with people who understand and validate your feelings. You don't have to navigate them alone."
    ],
    'isolated_lonely_alone_disconnected': [
        "Feeling isolated can be lonely, but remember that there are people who care about you and want to support you.",
        "Reach out to friends, family, or support groups. Connecting with others can help reduce feelings of isolation.",
        "Consider volunteering or joining community activities to meet new people and build a sense of belonging.",
        "Engage in activities that bring you joy and fulfillment, even if you're alone. Your happiness matters.",
        "Know that feeling isolated is temporary. Reach out and connect with others, even if it feels uncomfortable at first."
    ],
    'disconnected_detached_unattached_disengaged_uncoupled': [
        "Feeling disconnected can be disorienting, but remember that you're not alone. Reach out to trusted friends or family members for support.",
        "Engage in activities that bring you joy and connection, whether it's spending time with loved ones, pursuing hobbies, or volunteering.",
        "Practice mindfulness and grounding techniques to help you reconnect with the present moment and regain a sense of connection.",
        "Focus on building meaningful connections with others based on authenticity and mutual respect. You deserve relationships that nourish your soul.",
        "Explore new ways of connecting with others, whether it's through shared interests, experiences, or values. Your tribe is out there."
    ],
    'inadequate_insufficient_unqualified_unworthy_substandard': [
        "Feeling inadequate is tough, but remember that everyone has strengths and weaknesses. Focus on your unique talents and accomplishments.",
        "Challenge negative self-talk by practicing self-compassion and reminding yourself of your worth.",
        "Set realistic goals for yourself and celebrate your progress, no matter how small. You're capable of more than you realize.",
        "Surround yourself with people who uplift and encourage you. You deserve to be supported and celebrated.",
        "Focus on progress, not perfection. Each step forward is a testament to your resilience and determination."
    ],
    'unworthy_unvalued_disregarded': [
        "You are worthy of love and respect, regardless of what negative thoughts may say. Your value isn't determined by external measures.",
        "Practice self-compassion and kindness toward yourself. Treat yourself with the same care and understanding you would offer a friend.",
        "Challenge feelings of unworthiness by focusing on your strengths and achievements. You are enough, just as you are.",
        "Surround yourself with people who recognize and appreciate your worth. You deserve to be valued and respected.",
        "Focus on cultivating self-worth from within, rather than seeking external validation. You are inherently valuable, simply by being you."
    ],
    'burnout_exhaustion_fatigue_overwork_overwhelm': [
        "Experiencing burnout is tough, but it's important to prioritize self-care and set boundaries to prevent further exhaustion.",
        "Take time to rest and recharge. Engage in activities that bring you joy and relaxation.",
        "Consider seeking support from a therapist or counselor to help you cope with burnout and explore healthy coping strategies.",
        "Listen to your body's signals and honor your need for rest and replenishment. Your well-being is non-negotiable.",
        "Focus on finding balance in your life, even if it means saying no to additional responsibilities. Your health comes first."
    ],
    'exhausted_fatigued_weary_drained_spent': [
        "Feeling exhausted is draining, but remember to prioritize rest and self-care.",
        "Listen to your body and give yourself permission to take breaks when needed.",
        "Explore ways to reduce stress and recharge, whether it's through relaxation techniques, exercise, or spending time in nature.",
        "Set boundaries to protect your energy and well-being. It's okay to say no when you need to prioritize self-care.",
        "Find joy in simple pleasures that nourish your soul and replenish your energy. Sometimes, rest is the best medicine."
    ],
    'excluded_omitted_leftout_shunned_outcast': [
        "Feeling excluded is painful, but remember that your worth isn't determined by others' opinions or actions.",
        "Focus on building connections with people who appreciate and value you for who you are.",
        "Engage in activities and communities where you feel accepted and included. You deserve to be surrounded by supportive people.",
        "Recognize that exclusion often says more about others' insecurities than your own worth. You are enough, just as you are.",
        "Celebrate your uniqueness and individuality. The right people will recognize and celebrate you for who you are."
    ],
    'insecure_uncertain_unsure_inferior_vulnerable': [
        "Feeling insecure is challenging, but remember that you are worthy of love and acceptance just as you are.",
        "Challenge negative self-talk by focusing on your strengths and accomplishments.",
        "Practice self-compassion and kindness toward yourself. Treat yourself with the same understanding you would offer a friend.",
        "Surround yourself with people who uplift and support you. You deserve relationships that nurture your self-esteem.",
        "Focus on cultivating self-confidence from within, rather than seeking external validation. Your worth is inherent and undeniable."
    ],
    'indecisive_undecided_hesitant': [
        "Feeling indecisive can be frustrating, but remember that it's okay to take your time in making decisions.",
        "Consider breaking down complex decisions into smaller, more manageable steps.",
        "Trust your instincts and make choices that align with your values and goals.",
        "Seek input and advice from trusted friends or mentors when making decisions. Sometimes, an outside perspective can provide clarity.",
        "Embrace the process of decision-making as an opportunity for growth and self-discovery. Each choice you make shapes your journey."
    ],
    'overthinking_ruminating': [
        "Overthinking can be overwhelming, but try to focus on the present moment and avoid getting caught up in hypothetical scenarios.",
        "Practice mindfulness and grounding techniques to help you stay grounded and reduce rumination.",
        "Engage in activities that distract and relax your mind, such as exercise, creative pursuits, or spending time with loved ones.",
        "Challenge perfectionism and the need for certainty. Embrace the unknown and trust yourself to handle whatever comes your way.",
        "Set aside dedicated time for problem-solving and reflection, but also give yourself permission to let go of worries outside of those times."
    ],
    'self-conscious_awkward_uncomfortable_unease': [
        "Feeling self-conscious is common, but remember that everyone has insecurities. You are not alone in this.",
        "Focus on your strengths and unique qualities, rather than dwelling on perceived flaws.",
        "Practice self-compassion and kindness toward yourself. Treat yourself with the same care you would offer a friend.",
        "Surround yourself with supportive and accepting people who celebrate you for who you are. You deserve to feel valued and appreciated.",
        "Challenge negative self-perceptions by acknowledging your accomplishments and strengths. You are worthy of love and belonging."
    ],
    'unmotivated_indifferent_apathetic_uninspired': [
        "Experiencing a lack of motivation is tough, but remember that it's okay to take breaks and recharge.",
        "Set small, achievable goals for yourself and celebrate your progress along the way.",
        "Explore activities and pursuits that bring you joy and excitement. Sometimes, inspiration comes from unexpected places.",
        "Connect with your values and passions to reignite your sense of purpose and drive.",
        "Remember that motivation ebbs and flows. Be patient with yourself and trust that your motivation will return in time."
    ],
    'withdrawn_reclusive_retiring_antisocial_reserved': [
        "Feeling withdrawn can be isolating, but remember that it's okay to take time for yourself when needed.",
        "Reach out to trusted friends or family members for support and connection.",
        "Consider seeking professional help if you're struggling to engage with others or feel increasingly isolated.",
        "Engage in activities that bring you joy and fulfillment, even if you prefer solitude. Your happiness matters.",
        "Recognize that social withdrawal is a temporary coping mechanism. When you're ready, open yourself up to connection and community."
    ],
    'irritable_grumpy_cross_tetchy_peevish': [
        "Feeling irritable is challenging, but try to identify and address any underlying stressors or triggers.",
        "Practice relaxation techniques, such as deep breathing or meditation, to help calm your mind and body.",
        "Communicate your needs and feelings to others in a calm and respectful manner. Setting boundaries can help prevent conflicts.",
        "Explore the root causes of your irritability and address them proactively. Your well-being is worth the effort.",
        "Engage in activities that bring you joy and relaxation, even if you're feeling irritable. Self-care is especially important during difficult times."
    ],
    'resentful_bitter_rancorous_ill_disgruntled': [
        "Experiencing resentment is difficult, but try to address underlying issues and communicate your feelings openly and honestly.",
        "Practice forgiveness and compassion toward yourself and others. Holding onto resentment only harms yourself in the long run.",
        "Focus on finding constructive ways to address conflicts and grievances, rather than dwelling on negative emotions.",
        "Seek closure and resolution where possible, but also recognize that some situations may require acceptance and letting go.",
        "Remember that you have the power to choose how you respond to challenging situations. Choose kindness and compassion over resentment."
    ],
    'defensive_guarded_wary': [
        "Feeling defensive is natural, but try to approach conflicts and challenges with an open mind and willingness to listen.",
        "Practice active listening and empathy when engaging in difficult conversations. Seek to understand others' perspectives.",
        "Explore the underlying reasons behind your defensiveness and address any insecurities or fears that may be contributing to it.",
        "Focus on building trust and rapport in your relationships through honest communication and vulnerability.",
        "Recognize that defensiveness often stems from a desire to protect oneself. By fostering a sense of safety and security, you can reduce the need for defensiveness."
    ],
    'pessimistic_cynical_negative_disheartened': [
        "Feeling pessimistic is tough, but try to focus on finding silver linings and reasons to be hopeful.",
        "Challenge negative thought patterns by practicing gratitude and reframing setbacks as opportunities for growth.",
        "Surround yourself with positive influences, whether it's uplifting music, inspiring books, or supportive friends.",
        "Engage in activities that bring you joy and fulfillment, even if you're feeling pessimistic. Your happiness matters.",
        "Remember that optimism is a choice. By consciously choosing to focus on the positive, you can cultivate a more optimistic outlook over time."
    ],
    'paralyzed_frozen_stuck': [
        "Feeling paralyzed by indecision or fear is challenging, but try to take small steps toward your goals, even if they feel daunting.",
        "Break tasks into smaller, more manageable steps. Progress, no matter how small, is still progress.",
        "Practice self-compassion and kindness toward yourself. Be patient as you navigate through challenging times.",
        "Seek support from trusted friends, family, or professionals who can offer guidance and encouragement.",
        "Remember that it's okay to ask for help when you're feeling stuck. Sometimes, an outside perspective can provide clarity and direction."
    ],
    'angry_irritable_enraged_furious_outraged': [
        "Feeling angry is natural, but try to express your emotions in healthy and constructive ways.",
        "Take a break and step away from the situation if you need to calm down before addressing the issue.",
        "Practice relaxation techniques, such as deep breathing or progressive muscle relaxation, to help manage intense emotions.",
        "Communicate your feelings assertively and respectfully, focusing on finding solutions rather than placing blame.",
        "Explore the underlying causes of your anger and address them proactively. Your well-being is worth the effort."
    ]
}




def respond_mental_health(query):
    # Check for other keywords
    for keyword, responses in mental_health_dict.items():
        if any(word in query for word in keyword.split('_')):
            response = random.choice(responses)
            speak(response)
            return True
    
    # Check if the query contains the keyword "solution"
    if 'solution' in query:
        speak("Here are some general steps you can take to address your feelings:")
        speak("- Take deep breaths and try to calm yourself.")
        speak("- Practice mindfulness or meditation to help ground yourself.")
        speak("- Reach out to a trusted friend, family member, or mental health professional for support.")
        speak("- Engage in activities that bring you joy or relaxation, such as going for a walk, listening to music, or practicing a hobby.")
        speak("- Consider seeking professional help if your feelings persist or interfere with your daily life.")
        return True
    
    return False


if __name__ == "__main__":
    wishMe()
    loop_counter = 0
    max_attempts = 3
    while loop_counter < max_attempts:
        query = takeCommand()

        if query is not None:  # Check if query is not None
            query = query.lower()  # Convert query to lowercase
            loop_counter = 0
            if respond_mental_health(query):  # Check if it's a mental health query
                continue  # Skip further processing if it's a mental health
            

        else:
            loop_counter += 1

    if loop_counter == max_attempts:
        speak("No speech detected for more than three attempts. Exiting...")
    print("Exiting ")