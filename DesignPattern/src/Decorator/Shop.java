package Decorator;

public class Shop {
	public static void main(String[] args) {
	Beverage beverage = new Espresso();
	beverage = new Milk(beverage);
	System.out.println(beverage.getBeveragePrice());
	beverage = new Caramel(beverage);
	System.out.println(beverage.getBeveragePrice());
	}
}
