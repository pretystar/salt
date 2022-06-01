import { TestBed } from '@angular/core/testing';

import { SaltService } from './salt.service';

describe('SaltService', () => {
  let service: SaltService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SaltService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
