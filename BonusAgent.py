import openai

class SongLyricsAgent:
    def __init__(self, openai_api_key):
        self.api_key = openai_api_key
        openai.api_key = self.api_key

    def generate_song_lyrics(self, topic, mood="happy", keywords=[]):
        prompt = self._build_prompt(topic, mood, keywords)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a highly creative song lyricist."},
                {"role": "user", "content": prompt}
            ],
        )
        lyrics = response.choices[0].message["content"].strip()
        return lyrics

    def _build_prompt(self, topic, mood, keywords):
        prompt = f"Generate song lyrics about {topic}, conveying a {mood} mood."
        if keywords:
            prompt += " Incorporate the following keywords: " + ", ".join(keywords) + "."
        prompt += "\n\nLyrics:"
        return prompt

    def analyze_intent(self, user_input):
        lower_input = user_input.lower()
        if "song" in lower_input and "on" in lower_input:
            topic_start_index = lower_input.find("on") + 3
            topic = user_input[topic_start_index:].strip()
            if topic:
                return "generate_song_lyrics", topic
        return "unknown", None

if __name__ == "__main__":
    api_key = " Removed  for privacy reasons "
    agent = SongLyricsAgent(api_key)
    
    print("Hi! How can I assist you?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye! Have a nice day.")
            break
        
        intent, command = agent.analyze_intent(user_input)
        if intent == "generate_song_lyrics":
            topic = command
            print(f"Generating song lyrics about: {topic}")
            lyrics = agent.generate_song_lyrics(topic)
            print("Generated Song Lyrics:\n", lyrics)
        else:
            print("I'm not sure how to help with that. Please ask me to 'write a song on <topic>' or similar phrases.")
