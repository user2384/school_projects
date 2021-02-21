/*
 * File : ipk-sniffer.c
 * Project : Packet sniffer
 * Course : IPK (Computer Communications and Networks)
 * Author : Viktoria Haleckova
 */
#include <pcap.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <time.h>
#include <getopt.h>

#define SNAP_LEN 1518

/* link header length */
int linkhdrlen;

/* device for packet sniffing */
char dev[256] = "";

/* number of packets */
int num_packets = 1;

/* expression for port if used */
char port[256] = "port ";

/* expression for filter */
char filter_exp[256] = "";

/* structure for long option arguments */
static struct option long_options[] = {
    {"tcp", no_argument, NULL, 't'},
    {"udp", no_argument, NULL, 'u'},
    {NULL, 0, NULL, 0}
};

/*
 * Structure for ip header was inspired by:
 * Title : Create your own packet sniffer in C
 * Author : Varun Gupta
 * Availability : http://simplestcodings.blogspot.com/2010/10/create-your-own-packet-sniffer-in-c.html
 */
struct ip_struct {
    u_char ip_vhl;
    u_char ip_tos;
    u_short ip_len;
    u_short ip_id;
    u_short ip_off;
    #define IP_RF 0x8000
    #define IP_DF 0x4000
    #define IP_MF 0x2000
    #define IP_OFFMASK 0x1fff
    u_char ip_ttl;
    u_char ip_p;
    u_short ip_sum;
    struct in_addr ip_src, ip_dst;
};

#define IP_HL(ip) (((ip)->ip_vhl) & 0x0f)

/*
 * Structure for tcp header was inspired by:
 * Title : Create your own packet sniffer in C
 * Author : Varun Gupta
 * Availability : http://simplestcodings.blogspot.com/2010/10/create-your-own-packet-sniffer-in-c.html
 */
struct tcp_struct {
    u_short th_sport;
    u_short th_dport;
    u_int th_seq;
    u_int th_ack;
    u_char th_offx2;
    #define TH_OFF(th) (((th)->th_offx2 & 0xf0) >> 4)
    u_char th_flags;
    #define TH_FIN 0x01
    #define TH_SYN 0x02
    #define TH_RST 0x04
    #define TH_PUSH 0x08
    #define TH_ACK 0x10
    #define TH_URG     0x20
    #define TH_ECE 0x40
    #define TH_CWR 0x80
    #define TH_FLAGS (TH_FIN|TH_SYN|TH_RST|TG_ACK|TH_URG|TH_ECE|TH_CWR)
    u_short th_win;
    u_short th_sum;
    u_short th_urp;
};

/*
 * Function was inspired by:
 * Title : Create your own packet sniffer in C
 * Author : Varun Gupta
 * Availability : http://simplestcodings.blogspot.com/2010/10/create-your-own-packet-sniffer-in-c.html
 */
void print_hex_ascii_line(const u_char *payload, int len, int offset){
    int i;
    int gap;
    const u_char *ch;
    if (offset == 0)
        printf("0x0000 ");
    else
        printf("%#06x ", offset);
    ch = payload;
    for (i = 0; i < len; i++){
        printf("%02x ", *ch);
        ch++;
        if (i == 7)
            printf(" ");
    }
    if (len < 8)
        printf(" ");
    if (len < 16){
        gap = 16 - len;
        for (i = 0; i < gap; i++)
            printf("  ");
    }
    printf("  ");
        
    ch = payload;
    for (i = 0; i < len; i++){
        if (isprint(*ch))
            printf("%c", *ch);
        else
            printf(".");
        ch++;
    }

    printf("\n");
    return;
}

/*
 * Function was inspired by:
 * Title : Create your own packet sniffer in C
 * Author : Varun Gupta
 * Availability : http://simplestcodings.blogspot.com/2010/10/create-your-own-packet-sniffer-in-c.html
 */
void print_payload(const u_char *payload, int len){
    int len_rem = len;
    int line_width = 16;
    int line_len;
    int offset = 0;
    const u_char *ch = payload;
    if (len <= 0)
        return;
    if (len <= line_width){
        print_hex_ascii_line(ch, len, offset);
        return;
    }
    for (;;){
        line_len = line_width % len_rem;
        print_hex_ascii_line(ch, line_len, offset);
        len_rem = len_rem - line_len;
        ch = ch + line_len;
        offset = offset + line_width;
        if (len_rem <= line_width){
            print_hex_ascii_line(ch, len_rem, offset);
            break;
        }
    }
    return;
}

/*
 * Function was inspired by:
 * Title : Create your own packet sniffer in C
 * Author : Varun Gupta
 * Availability : http://simplestcodings.blogspot.com/2010/10/create-your-own-packet-sniffer-in-c.html
 */
void got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet){
    const struct ip_struct *ip;
    const struct tcp_struct *tcp;
    struct udphdr* udphdr;
    const char *payload;
    int size_ip;
    int size_tcp;
    int udpflag = 0;
    int size_payload;
    time_t timer;
    char buffer[26];
    struct tm* tm_info;
    timer = time(NULL);
    tm_info = localtime(&timer);
    strftime(buffer, 26, "%H:%M:%S",tm_info);
    ip = (struct ip_struct*)(packet + linkhdrlen);
    size_ip = IP_HL(ip)*4;
    if (size_ip < 20){
        printf("invalid header\n");
        return;
    }
    switch(ip->ip_p){
        case IPPROTO_TCP:
            break;
        case IPPROTO_UDP:
            udpflag = 1;
            break;
        case IPPROTO_ICMP:
            return;
        case IPPROTO_IP:
            return;
        default:
            return;
    }
    if (udpflag == 1){
        udphdr = (struct udphdr*)packet;
        printf("%s %s : %d > %s : %d\n", buffer, inet_ntoa(ip->ip_src), ntohs(udphdr->source), inet_ntoa(ip->ip_dst), ntohs(udphdr->dest));
        return;
    }
    tcp = (struct tcp_struct*)(packet + linkhdrlen + size_ip);
    size_tcp = TH_OFF(tcp)*4;
    if (size_tcp < 20){
        printf(" invalid header\n");
        return;
    }
    printf("%s %s : %d > %s : %d\n\n" , buffer, inet_ntoa(ip->ip_src), ntohs(tcp->th_sport), inet_ntoa(ip->ip_dst), ntohs(tcp->th_dport));
    payload = (u_char *)(packet + linkhdrlen + size_ip + size_tcp);
    size_payload = ntohs(ip->ip_len) - (size_ip + size_tcp);
    if (size_payload > 0){
        print_payload(payload, size_payload);
        printf("\n");
    }
    return;
}

/*
 * Function was inspired by:
 * Title : Develop a Packet Sniffer with Libpcap
 * Author : Vic Hargrave
 * Availability : https://vichargrave.github.io/programming/develop-a-packet-sniffer-with-libpcap/#compile-a-packet-capture-filter
 */
void capture_loop(pcap_t* pd){
    int linktype;
    if ((linktype = pcap_datalink(pd)) < 0){
        printf("pcap_datalink() %s\n",pcap_geterr(pd));
        return;
    }

    switch(linktype){
        case DLT_NULL:
            linkhdrlen = 4;
            break;
        case DLT_EN10MB:
            linkhdrlen = 14;
            break;
        case DLT_SLIP:
        case DLT_PPP:
            linkhdrlen = 24;
            break;
        default:
            printf("Unsupported datalink %d\n",linktype);
            return;
    }
}

/*
 * function finds all devices and prints them on standard output
 */
void get_all_devices(){
    char errbuf[PCAP_ERRBUF_SIZE]; /* error buffer */
    pcap_if_t *interfaces, *temp;
    int i = 1;
    if (pcap_findalldevs(&interfaces, errbuf) == -1){
            printf("Error while searching all devices\n");
            exit(1);
    }
    else{
        printf("Active interfaces:\n");
        for (temp = interfaces; temp; temp=temp->next)
            printf("%d. %s\n", i++, temp->name);
        exit(0);
    }
}

/*
 * function for parsing arguments
 * param @argc    number of arguments
 * param @argv    arguments
 */
void parse_args(int argc,char **argv){
    int pflag = 0;
    int iflag = 0;
    int c;
    while ((c = getopt_long(argc, argv, "hp:tui:n:", long_options, NULL)) != -1){
    switch(c){
            case 'h':
                printf("This is a simple packet sniffer application based on libpcap that displays packet information.\nUsage: ./ipk-sniffer -i interface [-p port] [--tcp|-t] [--udp|-u] [-n num]\n ");
                exit(0);
                break;
            case 'i':
                iflag = 1;
                strcpy(dev, optarg);
                break;
            case 'n':
                num_packets = atoi(optarg);
                break;
            case 'p':
                pflag = 1;
                strcat(port, optarg);
                break;
            case 't':
                strcpy(filter_exp, "tcp ");
                break;
            case 'u':
                strcpy(filter_exp, "udp ");
                break;
        }
    }

    /* if no interface was chosen */
    if (iflag == 0)
        get_all_devices();

    /* if port was chosen */
    if (pflag == 1)
        strcat(filter_exp, port);
}

int main(int argc, char **argv){
    pcap_t *handle; /* socket descriptor */
    struct bpf_program fp;
    bpf_u_int32 net; /* 32 bit net */
    bpf_u_int32 mask; /* 32 bit mask */
    char errbuf[PCAP_ERRBUF_SIZE]; /* error buffer */
    parse_args(argc, argv); /* parse input arguments */
    if (pcap_lookupnet(dev, &net, &mask, errbuf) == -1){
        printf("Error while getting net.\n");
        net = 0;
        mask = 0;
    }
    handle = pcap_open_live(dev, SNAP_LEN, 1, 1000, errbuf);
    if (handle == NULL){
        printf("Error while handling.\n");
        exit(1);
    }
    capture_loop(handle);
    if (pcap_compile(handle, &fp, filter_exp, 0, net) == -1){
        printf("Error while compiling filter.\n");
        exit(1);
    }
    if (pcap_setfilter(handle, &fp) == -1){
        printf("Error while setting filter.\n");
        exit(1);
    }
    pcap_loop(handle, num_packets, got_packet, NULL);
    pcap_freecode(&fp);
    pcap_close(handle);
    return 0;
}
