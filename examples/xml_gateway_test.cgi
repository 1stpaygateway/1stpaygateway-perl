###### XMLgatewaytest.cgi ###########################################
#
#This program is used to connect to the xml gateway api
#you will notice 6 variables named $xml_1 - $xml_6
#each variable contains the correctly formatted xml request required to send to the api 
#for each of the 6 operation types that can be performed.
#Each request can be altered by you to test the api and validate the responses you receive 
#back.
#You will also notice the two code snippets that handle seding the XML to the api
#and receiving the response back. Simply change which XML variable you want to
#either POST or GET to test the different operation types and responses
######### Explanation Over ########################################### 
#!c:\perl5\bin\perl.exe

use strict;
use warnings;

$|=1;

# Perl library modules
use WIN32::OLE;
use XML::Simple;

print "Content-type:text/html\n\n";

my $xml_1 = '<?xml version="1.0" encoding="UTF-8"?> 
<TRANSACTION>
	<FIELDS>
		<FIELD KEY="transaction_center_id">1264</FIELD>
		<FIELD KEY="gateway_id">a91c38c3-7d7f-4d29-acc7-927b4dca0dbe</FIELD> 
		<FIELD KEY="operation_type">sale</FIELD>
		<FIELD KEY="order_id">YOURID_NUMBER</FIELD>
		<FIELD KEY="total">5.00</FIELD>
		<FIELD KEY="card_name">Visa</FIELD>
		<FIELD KEY="card_number">4111111111111111</FIELD>
		<FIELD KEY="card_exp">1106</FIELD>
		<FIELD KEY="cvv2">123</FIELD>
		<FIELD KEY="owner_name">Bob Auth</FIELD>
		<FIELD KEY="owner_street">123 Test St</FIELD>
		<FIELD KEY="owner_city">city</FIELD>
		<FIELD KEY="owner_state">PA</FIELD>
		<FIELD KEY="owner_zip">12345-6789</FIELD>
		<FIELD KEY="owner_country">US</FIELD>
		<FIELD KEY="recurring">0</FIELD>
		<FIELD KEY="recurring_type">annually</FIELD>
	</FIELDS> 
</TRANSACTION>';

my $xml_2 = '<?xml version="1.0" encoding="UTF-8"?> 
<TRANSACTION>
	<FIELDS>
		<FIELD KEY="transaction_center_id">1264</FIELD>
		<FIELD KEY="gateway_id">a91c38c3-7d7f-4d29-acc7-927b4dca0dbe</FIELD> 
		<FIELD KEY="operation_type">credit</FIELD>
		<FIELD KEY="total_number_transactions">1</FIELD>
		<FIELD KEY="reference_number1">REF ID FROM SALE </FIELD>
		<FIELD KEY="credit_amount1">1.00</FIELD>
	</FIELDS> 
</TRANSACTION>';

my $xml_3 = '<?xml version="1.0" encoding="UTF-8"?> 
<TRANSACTION>
	<FIELDS>
		<FIELD KEY="transaction_center_id">1264</FIELD>
		<FIELD KEY="gateway_id">a91c38c3-7d7f-4d29-acc7-927b4dca0dbe</FIELD> 
		<FIELD KEY="operation_type">void</FIELD>
		<FIELD KEY="total_number_transactions">3</FIELD>
		<FIELD KEY="reference_number1">REF ID FROM AUTH</FIELD>
		<FIELD KEY="reference_number2">REF ID FROM AUTH</FIELD>
		<FIELD KEY="reference_number3">REF ID FROM AUTH</FIELD>
	</FIELDS> 
</TRANSACTION>';

my $xml_4 = '<?xml version="1.0" encoding="UTF-8"?> 
<TRANSACTION>
	<FIELDS>
		<FIELD KEY="transaction_center_id">1264</FIELD>
		<FIELD KEY="gateway_id">a91c38c3-7d7f-4d29-acc7-927b4dca0dbe</FIELD> 
		<FIELD KEY="operation_type">settle</FIELD>
		<FIELD KEY="total_number_transactions">2</FIELD>
		<FIELD KEY="reference_number1">REF ID FROM AUTH</FIELD>
		<FIELD KEY="settle_amount1">5.00</FIELD>
		<FIELD KEY="reference_number2">REF ID FROM AUTH</FIELD>
		<FIELD KEY="settle_amount2">2.00</FIELD>
	</FIELDS> 
</TRANSACTION>';

my $xml_5 = '
<?xml version="1.0" encoding="UTF-8"?> 
<TRANSACTION>
	<FIELDS>
		<FIELD KEY="transaction_center_id">1264</FIELD>
		<FIELD KEY="gateway_id">a91c38c3-7d7f-4d29-acc7-927b4dca0dbe</FIELD> 
		<FIELD KEY="operation_type">auth</FIELD>
		<FIELD KEY="order_id">YOURID_NUMBER</FIELD>
		<FIELD KEY="total">5.00</FIELD>
		<FIELD KEY="card_name">Visa</FIELD>
		<FIELD KEY="card_number">4111111111111111</FIELD>
		<FIELD KEY="card_exp">1006</FIELD>
		<FIELD KEY="cvv2">123</FIELD>
		<FIELD KEY="owner_name">Bob Recurring_Sale</FIELD>
		<FIELD KEY="owner_street">123 test st</FIELD>
		<FIELD KEY="owner_city">city</FIELD>
		<FIELD KEY="owner_state">PA</FIELD>
		<FIELD KEY="owner_zip">12345-6789</FIELD>
		<FIELD KEY="owner_country">US</FIELD>
		<FIELD KEY="recurring">0</FIELD>
		<FIELD KEY="recurring_type"></FIELD>
	</FIELDS> 
</TRANSACTION>';

my $xml_6 = '<?xml version="1.0" encoding="UTF-8"?> 
<TRANSACTION>
	<FIELDS>
		<FIELD KEY="transaction_center_id">1264</FIELD>
		<FIELD KEY="gateway_id">a91c38c3-7d7f-4d29-acc7-927b4dca0dbe</FIELD> 
		<FIELD KEY="operation_type”>query</FIELD>
		<FIELD KEY="card_type"></FIELD>
		<FIELD KEY="trans_type">SALE</FIELD>
		<FIELD KEY="trans_status">0</FIELD>
		<FIELD KEY="begin_date">100103</FIELD>
		<FIELD KEY="begin_time">1222AM</FIELD>
		<FIELD KEY="end_date">123103</FIELD>
		<FIELD KEY="end_time">1159PM</FIELD> 
		<FIELD KEY="order_id"></FIELD>
		<FIELD KEY="card_number"></FIELD> 
		<FIELD KEY="low_amount"></FIELD> 
		<FIELD KEY="high_amount"></FIELD>
	</FIELDS> 
</TRANSACTION>';

my $SendObject = Win32::OLE->new('microsoft.XMLhttp');

$SendObject->open("POST", "https://secure.1stpaygateway.net/secure/gateway/xmlgateway.aspx", "false"); 
$SendObject->setRequestHeader("Content-type", "text/xml");
$SendObject->send();
my $response = $SendObject->responseText;

print "<html><head><title>testing xml gateway</title><head><body>"; 
print "GET RESPONSE: $response";

#contains key value pairs of xml returned
my %xml_pairs_get = &ParseXml($response);

$SendObject->open("POST", "https://secure.1stpaygateway.net/secure/gateway/xmlgateway.aspx ", "false"); 
$SendObject->setRequestHeader("Content-type", "text/xml");

$SendObject->send($xml_2);
$response = $SendObject->responseText;

print "<br><br>POST RESPONSE: $response";

#contains key value pairs of xml returned
my %xml_pairs_post = &ParseXml($response);

print "</body></html>";

#this method will parse the xml and return a hash of key value pairs 
#which can be manipulated in any way you need them to be
sub ParseXml {
	my $xml = $_[0];
	my %RESULT;
	my $ref = eval { XMLin($xml) }; 
	if ($@) {
		$RESULT{error} = $@; 
		return(%RESULT);
	}

	foreach my $key(@{$ref->{'FIELDS'}{'FIELD'}}) { 
		my ($val1, $val2) = each %$key;
		my ($val3, $val4) = each %$key;
		my ($val5, $val6) = each %$key;
		if($val5 && $val6){
			$RESULT{$val6} = $val4;
		} else {
			$RESULT{$val4} = $val2;
		} 
	}
	return(%RESULT);
}

#EOF