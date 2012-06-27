<?php

// Include the API binding
require_once 'twfyapi.php';

// Set up a new instance of the API binding
$twfyapi = new TWFYAPI('En4awbDbbM78F9BCSGEKdWeE');

// Get a list of Labour MPs in XML format
//$mpsJson = $twfyapi->query('getMPs', array('output' => 'js'));

//$mpsJson = utf8_encode($mpsJson);

//$mpsArr = json_decode($mpsJson,true);

//var_dump($mpsArr);exit();

//$mp_pop = (json_decode(file_get_contents('mp-pop.json'), true));

//$count = count($mp_pop);
//$mp_pop = array_slice($mp_pop, ($count-120), 10);
//$mp_pop = array_slice($mp_pop, 110, 11);
//var_dump($mp_pop);exit;


//$mpsArrTest = array_slice($mpsArr,  0 , 4, true);
$mp_pop[] = array(
	'total_results' => '5570',
	'name' => 'David Cameron',
	'person_id' => '10777'
);
$mp_pop[] = array(
	'total_results' => '6608',
	'name' => 'Vincent Cable',
	'person_id' => '10084'
);
$mp_pop[] = array(
	'total_results' => '2227',
	'name' => 'Nicholas Clegg',
	'person_id' => '11812'
);
$mp_pop[] = array(
	'total_results' => '6980',
	'name' => 'David Miliband',
	'person_id' => '11113'
);
$mp_pop[] = array(
	'total_results' => '2232',
	'name' => 'Edward Miliband',
	'person_id' => '11545'
);
$mp_pop[] = array(
	'total_results' => '5982',
	'name' => 'Theresa May',
	'person_id' => '10426'
);
foreach($mp_pop as $mp){
	//echo "data.addColumn('number', '".$mp['name']."');\n";
}
//exit();

$dates = array();
$hansards = array();
$n = 1;
foreach($mp_pop as $mp){
	$hansard = $twfyapi->query('getHansard', array('output' => 'js', 'person' => $mp['person_id'], 'num' => $mp['total_results']));
	
	$hansards[] = json_decode(utf8_encode($hansard), true);
	$mpRefs[$mp['person_id']] = $n;
	$n++;

}
$n = 0;
foreach($hansards as $hansard){
	foreach($hansard['rows'] as $row){
		$date = substr($row['hdate'],0,7);
		if(isset($dateRefs[$date])){// or intval($date) < 2009){
			//do nothing
		} else {
			$dateRefs[$date] = $n;
			$dates[$n][0] = $date;
			$n++;
		}
	}
}
$n = 0;
foreach($dates as $date){
	$i = 1;
	foreach($mpRefs as $k => $v){
		$dates[$n][$v] = null;
	$i++;
	}
$n++;
}
$n = 0;
foreach($hansards as $hansard){
	//var_dump($hansard);exit();
	foreach($hansard['rows'] as $row){
		$date = substr($row['hdate'],0,7);
		$mpid = substr($hansard['info']['s'],8);
		//if(intval($date) >= 2009){
			$dateRef = $dateRefs[$date];
			$mpRef = $mpRefs[$mpid];
			$dates[$dateRef][$mpRef]++;
		//}
	}
}

foreach($dates as $k => $v){
	$c = 0;
	$t = 0;
	$avArr = array_slice($v,1);
	foreach($avArr as $mpc){
		$c++;
		$t = $t+$mpc;
	}
	$dates[$dateRefs[$v[0]]][] = $t/$c;
}

sort($dates);

echo json_encode($dates);


?>
