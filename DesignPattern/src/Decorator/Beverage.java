package Decorator;

public abstract class Beverage {

	String beverageName = "";
	int beveragePrice = 0;
	
	public String getBeverageName() {
		return beverageName;
	}
	
	//public abstract int getBeveragePrice();
	
	public int getBeveragePrice() {
		return beveragePrice;
	}

	public void setBeverageName(String beverageName) {
		this.beverageName = beverageName;
	}

	public void setBeveragePrice(int beveragePrice) {
		this.beveragePrice = beveragePrice;
	}
	
	
}
