from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Inputs:
    km : float
    Length : float
    Width : float
    Height : float
    KerbWeight : float
    TopSpeed : float
    Acceleration : float
    CargoVolumn : float
    mileage_new : float
    AlloyWheelSize : float
    MaxPowerbhp : float
    MaxPowerRPM : float
    MaxTorqueNm : float
    MaxTorqueRPM : float
    Displacement : float
    NoofCylinder : float
    SeatingCapacity : float
    car_age : float
    ft : object
    model : object
    transmissionType : object
    pageType : object
    carType : object
    Color : object
    ValueConfiguration : object
    TurboCharger : object
    SuperCharger : object
    GearBox : object
    DriveType : object
    SteeringType : object
    FrontBrakeType : object
    RearBrakeType : object
    TyreType : object
    seller_type_new : object
    state : object
    car_segment : object
    owner_type : object
    vid: Optional[object] = None
