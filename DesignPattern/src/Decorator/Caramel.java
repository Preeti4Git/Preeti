package Decorator;

public class Caramel extends IngredientDecorator{
	
	public Caramel(Beverage beverage) {
		this.beverage = beverage;		
	}

	@Override
	public String getBeverageName() {
		// TODO Auto-generated method stub
		return beverage.getBeverageName()+"with Caramel";
	}

	@Override
	public void setBeverageName(String beverageName) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public int getBeveragePrice() {
		// TODO Auto-generated method stub
		return beverage.getBeveragePrice()+5;
	}

	@Override
	public void setBeveragePrice(int beveragePrice) {
		// TODO Auto-generated method stub
		
	}
	
	

}
