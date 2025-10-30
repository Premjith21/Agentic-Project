from .base_agent import BaseAgent
import yfinance as yf

class FinanceAgent(BaseAgent):
    def get_agent_name(self):
        return "Finance Agent"
    
    def should_handle(self, message: str) -> bool:
        finance_keywords = [
            'stock', 'price', 'finance', 'investment', 'market', 'bitcoin',
            'crypto', 'currency', 'money', 'bank', 'loan', 'interest', 'compound',
            'savings', 'budget', 'economy', 'trading', 'invest', 'portfolio',
            'dividend', 'revenue', 'profit', 'loss', 'asset', 'liability',
            'balance sheet', 'income statement', 'cash flow', 'roi', 'return',
            'mutual fund', 'etf', 'bond', 'security', 'option', 'future',
            'hedge fund', 'venture capital', 'ipo', 'merger', 'acquisition'
        ]
        return any(keyword in message.lower() for keyword in finance_keywords)
    
    def handle_message(self, message: str, context: dict = None) -> str:
        # Only extract stock symbol if message is clearly about stock prices
        symbol = self.extract_stock_symbol(message)
        if symbol and self.is_stock_price_query(message):
            stock_data = self.get_stock_data(symbol)
            if stock_data:
                return self.format_stock_response(stock_data, symbol)
        
        system_msg = "You are a financial expert. Provide accurate financial information and market insights about stocks, investments, banking, and economic concepts."
        prompt = f"Provide financial information about: {message}"
        return self.call_llm(prompt, system_msg)
    
    def extract_stock_symbol(self, message: str):
        words = message.upper().split()
        common_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA', 'BTC', 'ETH']
        for word in words:
            if word in common_symbols:
                return word
        return None
    
    def is_stock_price_query(self, message: str) -> bool:
        """Check if the query is specifically about stock prices"""
        price_indicators = ['stock', 'price', 'share price', 'trading', 'market price', 'current price']
        message_lower = message.lower()
        return any(indicator in message_lower for indicator in price_indicators)
    
    def get_stock_data(self, symbol: str):
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            history = stock.history(period="1d")
            
            if history.empty:
                return None
                
            return {
                'current_price': history['Close'].iloc[-1],
                'change': history['Close'].iloc[-1] - history['Open'].iloc[0],
                'company_name': info.get('longName', 'N/A')
            }
        except:
            return None
    
    def format_stock_response(self, data: dict, symbol: str) -> str:
        change_percent = (data['change'] / (data['current_price'] - data['change'])) * 100
        change_dir = "+" if data['change'] >= 0 else ""
        
        return f"""Stock Information for {symbol} ({data['company_name']}):
• Current Price: ${data['current_price']:.2f}
• Change: {change_dir}${data['change']:.2f} ({change_dir}{change_percent:.2f}%)"""