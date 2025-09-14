from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import yfinance as yf
import matplotlib.pyplot as plt

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
    
class YFinanceSearchTool(BaseTool): 

    name: str = "YFinanceSearchTool"
    description: str = "Fetches historical stock price data from Yahoo Finance given a ticker symbol and date range."

    def _run(self, ticker: str, start_date: str, end_date: str) -> str: #_run method is used since crewai will automatically call the inputs after running it
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(start=start_date, end=end_date)

            if history.empty:
                return f"No data found for {ticker} between {start_date} and {end_date}."
            
            plt.plot(history.index, history['Close'])
            plt.title(f"{ticker} Stock Prices")
            plt.xlabel("Date")
            plt.ylabel("Closing Price")
            plt.savefig("stock_chart.png")

            return history['Close'].to_json()
        except Exception as e:
            return f"Error fetching stock data: {e}"

