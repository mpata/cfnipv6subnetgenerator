import cfnresponse
import ipaddress
import uuid


def subnetgenerator(event):
    """Generate IPv6 Subnets

    Required keys inside event["ResourceProperties"]:
        - Ipv6CidrBlock
    Optional keys:
        - Count (default: 1)
        - Prefix (default: 64)

    Args:
        event(dict): Lambda function event

    Returns:
        list: List of strings (subnets)
    """
    if "Ipv6CidrBlock" not in event["ResourceProperties"]:
        raise Exception("No Ipv6CidrBlock specified")
    ipv6cidrblock = ipaddress.IPv6Network(
                unicode(event["ResourceProperties"]["Ipv6CidrBlock"]))
    if "Prefix" not in event["ResourceProperties"]:
        prefix = 64
    else:
        prefix = int(event["ResourceProperties"]["Prefix"])
        if (prefix <= ipv6cidrblock.prefixlen):
            raise Exception("Prefix must be higher than '{prefixlen}'".format(
                prefixlen=ipv6cidrblock.prefixlen))
    if "Count" not in event["ResourceProperties"]:
        count = 1
        event["ResourceProperties"] = 1
    else:
        count = int(event["ResourceProperties"]["Count"])
    subnets = []
    for subnet in ipv6cidrblock.subnets(new_prefix=prefix):
        if count == 0:
            break
        subnets.append(str(subnet))
        count -= 1
    if count > 0:
        raise Exception("Chosen prefix '{prefixlen}' doesn't allow the "
                        "creation of the requested '{count}' subnets".format(
                            prefixlen=ipv6cidrblock.prefixlen,
                            count=event["ResourceProperties"]["Count"]))
    return(subnets)


def lambda_handler(event, context):
    if event["RequestType"] in ["Create", "Update"]:
        try:
            subnets = subnetgenerator(event)
        except:
            cfnresponse.send(
                event,
                context,
                cfnresponse.FAILED,
                None,
                event["PhysicalResourceId"] or None)
            return
        cfnresponse.send(
            event,
            context,
            cfnresponse.SUCCESS,
            {"Subnets": subnetgenerator(event)},
            str(uuid.uuid4()))
    elif event["RequestType"] == "Delete":
        cfnresponse.send(
            event,
            context,
            cfnresponse.SUCCESS,
            None,
            event["PhysicalResourceId"])
    else:
        raise Exception("Unknown RequestType %s" % (event["RequestType"]))
