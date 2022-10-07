package Preeti;

import java.util.Base64;

public class Encode {

	/*
	 * public static String Base64Encode(String plainText) { var plainTextBytes =
	 * System.Text.Encoding.UTF8.GetBytes(plainText); return
	 * System.Convert.ToBase64String(plainTextBytes); }
	 * 
	 * byte[] encodedBytes = Base64.encodeBase64("Test".getBytes());
	 * System.out.println("encodedBytes " + new String(encodedBytes)); byte[]
	 * decodedBytes = Base64.decodeBase64(encodedBytes);
	 * System.out.println("decodedBytes " + new String(decodedBytes));
	 */
	public static void main(String[] args) {
	String encodeBytes = Base64.getEncoder().encodeToString(("du" + ":" + "VW2sa6uS5p53wiqsq65Coe4wdkuC7E").getBytes());
	System.out.println(encodeBytes); //ZHU6Vlcyc2E2dVM1cDUzd2lxc3E2NUNvZTR3ZGt1QzdF
	byte[] encodeByteArray = Base64.getEncoder().encode(("du" + ":" + "VW2sa6uS5p53wiqsq65Coe4wdkuC7E").getBytes());
	System.out.println(encodeByteArray.length);
	//System.out.println(encodeBytes);
	//String basicAuthenticationHeader = Convert.ToBase64String(Encoding.GetEncoding("ISO-8859-1").GetBytes("du:VW2sa6uS5p53wiqsq65Coe4wdkuC7E"));
	//System.out.println(basicAuthenticationHeader);
	}
}
