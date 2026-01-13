#!/usr/bin/env python3
"""
MCP Server for TU Dresden Canteen API (OpenMensa v2)
Provides tools to query canteen information, available days, and daily menus.
"""

import asyncio
import httpx
from datetime import datetime

from mcp.server.fastmcp import FastMCP

# Base URL for the OpenMensa API
BASE_URL = "https://api.studentenwerk-dresden.de/openmensa/v2"

# Initialize the MCP server
mcp = FastMCP("mensa-tud-mcp")

@mcp.tool()
async def list_canteens() -> str:
    """List all available canteens from the Studentenwerk Dresden.
    
    Returns canteen IDs, names, addresses, and coordinates for all available canteens.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/canteens")
            response.raise_for_status()
            canteens = response.json()
            
            # Format the output
            result = "Available Canteens:\n\n"
            for canteen in canteens:
                result += f"ID: {canteen.get('id')}\n"
                result += f"Name: {canteen.get('name')}\n"
                result += f"City: {canteen.get('city', 'N/A')}\n"
                result += f"Address: {canteen.get('address', 'N/A')}\n"
                
                if 'coordinates' in canteen and canteen['coordinates']:
                    coords = canteen['coordinates']
                    result += f"Coordinates: {coords[0]}, {coords[1]}\n"
                
                result += "\n" + "-" * 50 + "\n\n"
            
            return result
        
        except httpx.HTTPError as e:
            return f"HTTP Error: {str(e)}"


@mcp.tool()
async def list_canteen_days(canteen_id: int) -> str:
    """List all days for which a canteen has meal data available.
    
    Args:
        canteen_id: The ID of the canteen to query (e.g., 9 for Alte Mensa)
    
    Returns dates for which you can query meals.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/canteens/{canteen_id}/days")
            response.raise_for_status()
            days = response.json()
            
            # Format the output
            result = f"Available days for canteen {canteen_id}:\n\n"
            
            if not days:
                result += "No days available.\n"
            else:
                for day in days:
                    date = day.get('date')
                    closed = day.get('closed', False)
                    status = "CLOSED" if closed else "OPEN"
                    # Parse date to get weekday name
                    date_obj = datetime.strptime(date, "%Y-%m-%d")
                    weekday = date_obj.strftime('%A')
                    result += f"{date} ({weekday}): {status}\n"
            
            return result
        
        except httpx.HTTPError as e:
            return f"HTTP Error: {str(e)}"


@mcp.tool()
async def get_meals(canteen_id: int, date: str | None = None) -> str:
    """Get all meals available at a specific canteen on a specific date.

    Notes: 
    * To figure out the ID of a specific canteen, first use the `list_canteens` tool.
    * Also make sure to check which days have meal data available using the `list_canteen_days` tool.
    
    Args:
        canteen_id: The ID of the canteen to query (e.g., 9 for Alte Mensa)
        date: The date in YYYY-MM-DD format (e.g., 2026-01-13). If not provided, uses today's date.
    
    Returns meal names, categories, prices, and dietary information.
    """
    if not date:
        # Use today's date if not provided
        date = datetime.now().strftime("%Y-%m-%d")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/canteens/{canteen_id}/days/{date}/meals")
            response.raise_for_status()
            meals = response.json()
            
            # Format the output
            result = f"Meals for canteen {canteen_id} on {date}:\n\n"
            
            if not meals:
                result += "No meals available for this date.\n"
            else:
                for meal in meals:
                    result += f"Name: {meal.get('name', 'N/A')}\n"
                    result += f"Category: {meal.get('category', 'N/A')}\n"
                    
                    # Prices
                    prices = meal.get('prices', {})
                    if prices:
                        result += "Prices:\n"
                        for price_type, price in prices.items():
                            if price:
                                result += f"  {price_type}: €{price:.2f}\n"
                    
                    # Notes (dietary information, allergens, etc.)
                    notes = meal.get('notes', [])
                    if notes:
                        result += f"Notes: {', '.join(notes)}\n"
                    
                    result += "\n" + "-" * 50 + "\n\n"
            
            return result
        
        except httpx.HTTPError as e:
            return f"HTTP Error: {str(e)}"


def main():
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
