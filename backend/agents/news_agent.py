from .base_agent import BaseAgent
import requests
import os

class NewsAgent(BaseAgent):
    def get_agent_name(self):
        return "News Agent"
    
    def should_handle(self, message: str) -> bool:
        message_lower = message.lower()
        
        # Expanded news and current events keywords
        news_keywords = [
            'news', 'headlines', 'latest', 'update', 'breaking', 'current events',
            'politics', 'business', 'sports', 'technology', 'tech', 'entertainment',
            'health', 'science', 'world', 'national', 'local', 'headline', 'report',
            'coverage', 'journalism', 'media', 'press', 'bulletin', 'alert',
            'developments', 'happening', 'occurring', 'incident', 'event'
        ]
        
        # Check for news keywords
        if any(keyword in message_lower for keyword in news_keywords):
            return True
        
        # Check for category-specific content that indicates news interest
        category_indicators = [
            # Sports
            'football', 'basketball', 'soccer', 'baseball', 'tennis', 'cricket', 'golf',
            'nfl', 'nba', 'mlb', 'nhl', 'fifa', 'uefa', 'tournament', 'match', 'game',
            'score', 'player', 'team', 'championship', 'olympics', 'athlete', 'coach',
            'stadium', 'arena', 'victory', 'defeat', 'record', 'statistics',
            # Entertainment
            'movie', 'film', 'tv', 'television', 'celebrity', 'hollywood', 'oscar',
            'grammy', 'award', 'nomination', 'premiere', 'release', 'netflix',
            'disney', 'marvel', 'actor', 'actress', 'singer', 'band', 'album',
            'cinema', 'theater', 'director', 'producer', 'box office', 'trailer',
            'red carpet', 'festival', 'broadway', 'series', 'episode', 'season',
            # Technology
            'apple', 'google', 'microsoft', 'iphone', 'android', 'ai', 'software',
            'update', 'announcement', 'launch', 'product', 'computer', 'gadget',
            'robot', 'drone', 'virtual reality', 'blockchain', 'crypto',
            # Business
            'stock', 'market', 'finance', 'economy', 'company', 'investment',
            'bank', 'money', 'trading', 'revenue', 'profit', 'ceo', 'executive',
            # Health
            'medical', 'health', 'hospital', 'doctor', 'disease', 'treatment',
            'vaccine', 'research', 'study', 'patient', 'fitness', 'wellness',
            # Science
            'science', 'space', 'nasa', 'research', 'discovery', 'climate',
            'environment', 'physics', 'chemistry', 'biology', 'astronomy',
            # Politics
            'government', 'election', 'congress', 'senate', 'president', 'law',
            'policy', 'democrat', 'republican', 'vote', 'campaign'
        ]
        
        # If message contains category indicators, it's likely news-related
        if any(indicator in message_lower for indicator in category_indicators):
            return True
        
        return False
    
    def handle_message(self, message: str, context: dict = None) -> str:
        category = self.extract_category(message)
        news_data = self.get_news_data(category)
        
        if news_data:
            return self.format_news_response(news_data, category)
        else:
            system_msg = "You are a news reporter. Provide current news and updates."
            prompt = f"Tell me about recent news regarding: {message}"
            return self.call_llm(prompt, system_msg)
    
    def extract_category(self, message: str) -> str:
        message_lower = message.lower()
        
        category_mapping = {
            'sports': [
                'sports', 'football', 'basketball', 'soccer', 'baseball', 'tennis', 
                'olympics', 'nfl', 'nba', 'mlb', 'hockey', 'cricket', 'golf', 
                'athlete', 'game', 'match', 'tournament', 'championship', 'score',
                'player', 'team', 'league', 'super bowl', 'world cup', 'nhl',
                'fifa', 'uefa', 'premier league', 'champions league', 'ncaa',
                'playoff', 'final', 'semifinal', 'quarterfinal', 'victory', 'defeat',
                'coach', 'training', 'stadium', 'arena', 'olympic', 'paralympic',
                'medal', 'gold', 'silver', 'bronze', 'record', 'statistics'
            ],
            'entertainment': [
                'entertainment', 'movie', 'music', 'celebrity', 'hollywood', 
                'tv', 'film', 'actor', 'actress', 'singer', 'band', 'album',
                'release', 'premiere', 'oscar', 'grammy', 'award', 'show',
                'netflix', 'disney', 'marvel', 'star wars', 'cinema', 'theater',
                'director', 'producer', 'screen', 'box office', 'trailer',
                'nomination', 'red carpet', 'festival', 'broadway', 'comedy',
                'drama', 'action', 'horror', 'romance', 'documentary', 'series',
                'episode', 'season', 'preview', 'review', 'critic', 'rating',
                'soundtrack', 'concert', 'tour', 'performance', 'exhibition'
            ],
            'technology': [
                'tech', 'technology', 'computer', 'software', 'ai', 
                'artificial intelligence', 'gadget', 'iphone', 'android',
                'google', 'microsoft', 'apple', 'facebook', 'twitter', 'instagram',
                'internet', 'web', 'digital', 'innovation', 'startup', 'app',
                'robot', 'drone', 'virtual reality', 'blockchain', 'crypto',
                'iphone', 'ipad', 'macbook', 'windows', 'linux', 'programming',
                'developer', 'code', 'update', 'announcement', 'launch', 'product'
            ],
            'business': [
                'business', 'finance', 'economy', 'market', 'stock', 
                'investment', 'money', 'bank', 'company', 'corporate', 'enterprise',
                'entrepreneur', 'startup', 'wall street', 'trading', 'exchange',
                'revenue', 'profit', 'loss', 'merger', 'acquisition', 'deal',
                'ceo', 'executive', 'board', 'share', 'dividend', 'ipo'
            ],
            'health': [
                'health', 'medical', 'medicine', 'hospital', 'doctor', 'nurse',
                'fitness', 'wellness', 'disease', 'treatment', 'vaccine', 'clinic',
                'nutrition', 'diet', 'exercise', 'mental health', 'therapy',
                'surgery', 'patient', 'healthcare', 'pharmacy', 'drug', 'pill'
            ],
            'science': [
                'science', 'research', 'discovery', 'space', 'nasa', 'esa',
                'climate', 'environment', 'physics', 'chemistry', 'biology',
                'astronomy', 'planet', 'universe', 'experiment', 'laboratory',
                'scientist', 'researcher', 'theory', 'hypothesis', 'evidence'
            ],
            'politics': [
                'politics', 'government', 'election', 'congress', 'senate',
                'president', 'prime minister', 'law', 'policy', 'democrat',
                'republican', 'vote', 'campaign', 'international', 'diplomacy',
                'treaty', 'summit', 'parliament', 'senator', 'representative'
            ]
        }
        
        # Check categories in priority order
        for category, keywords in category_mapping.items():
            if any(keyword in message_lower for keyword in keywords):
                return category
        
        return 'general'  # Default category
    
    def get_news_data(self, category: str = 'general'):
        api_key = os.getenv('NEWS_API_KEY')
        if not api_key:
            return None
            
        try:
            # Build URL with category if specified
            if category == 'general':
                url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
            else:
                url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api_key}"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                return articles[:5]  # Return top 5 articles
            else:
                print(f"News API error: {response.status_code}")
                return None
        except Exception as e:
            print(f"News API exception: {e}")
            return None
    
    def format_news_response(self, articles: list, category: str) -> str:
        if not articles:
            return f"❌ No {category} news available at the moment."
        
        category_display = category.title() if category != 'general' else 'Latest'
        response = f"📰 {category_display} News Headlines:\n\n"
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'No title')
            source = article.get('source', {}).get('name', 'Unknown source')
            response += f"{i}. {title} - {source}\n"
        
        return response