import oci

configfile = "~/.oci/config"

config = oci.config.from_file(configfile)
identity = oci.identity.IdentityClient(config)
search = oci.resource_search.ResourceSearchClient(config)
networking = oci.core.VirtualNetworkClient(config)

RootCompartmentID = config["tenancy"]
region = config["region"]

Tenancy = identity.get_tenancy(tenancy_id=RootCompartmentID).data
user = identity.get_user(config["user"]).data
userName = user.description

print("Logged in as: {}/{} @ {}".format(userName, Tenancy.name, region))

query = "query subnet resources"

sdetails = oci.resource_search.models.StructuredSearchDetails()
sdetails.query = query

result = search.search_resources(search_details=sdetails, limit=1000).data

for subnet in result.items:
    print ("Subnet: {}".format(subnet.display_name))
    subnetdetails = networking.get_subnet(subnet_id=subnet.identifier).data
    cidr = subnetdetails.cidr_block
    a,b = cidr.split("/")
    totalips = 2**(32-int(b))
    ips = networking.list_private_ips(subnet_id=subnet.identifier).data
    for ip in ips:
        print (" - {} - {}".format(ip.display_name, ip.ip_address))
    print (" Total IPS: {}  Used IPs: {}  Available IPs: {}".format(totalips, len(ips), totalips-len(ips)-3))
    print (" ")




