package Decorator;

public class Milk extends IngredientDecorator{
	
	//private Beverage beverage;

	public Milk(Beverage beverage) {
		this.beverage = beverage;		
	}

	@Override
	public String getBeverageName() {
		// TODO Auto-generated method stub
		return beverage.getBeverageName()+"with milk";
	}

	@Override
	public void setBeverageName(String beverageName) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public int getBeveragePrice() {
		// TODO Auto-generated method stub
		return beverage.getBeveragePrice()+2;
	}

	@Override
	public void setBeveragePrice(int beveragePrice) {
		// TODO Auto-generated method stub
		
	}

}
