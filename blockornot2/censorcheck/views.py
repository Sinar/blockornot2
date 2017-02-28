from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from censorcheck.models import OONIRecord
from django.db.models import Max
from urllib import urlencode
from django.core.urlresolvers import reverse


class SearchView(View):
    def get(self, request):
        q = request.GET.get("q")
        results = []
        if q:
            query =  OONIRecord.objects.filter(input_url__contains=q)
            records = query.values('input_url').distinct()
            for record in records:
                links = reverse("detail") + "?" + urlencode({"q":record["input_url"] })
                temp = { "url": record["input_url"], "links": links } 
                results.append(temp)

        return render(request, "search.html", {"results":results}) 


class DetailView(View):
    def get(self, request):
        # Maybe get is a bad idea
        q = request.GET.get("q")
        if not q:
            return HttpResponse("Error")

        # I wonder if we can simplify the command
        # I did a group by on sqlite, it record latest result, not quite what I want
        query = OONIRecord.objects.filter(input_url=q)
        
        data = query.values("probe_asn").distinct()
        results = []
        for probe_asn in data:
            entries = query.filter(probe_asn=probe_asn["probe_asn"]).order_by("test_start_time")
            entry = entries[0]
            isp = { "isp": entry.probe_asn, "status": entry.status, "test_time": entry.test_start_time }
            results.append(isp)
        context = { "url": q, "isps": results }

        return render(request, "detail.html", context)


